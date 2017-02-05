from datetime import datetime
from pytz import UTC
from ordering.core import get_current_order_round, \
    update_totals_for_products_with_max_order_amounts
from ordering.models import OrderProduct
from ordering.tests.factories import OrderRoundFactory, OrderFactory, \
    ProductFactory, OrderProductFactory, ProductStockFactory
from vokou.testing import VokoTestCase


class TestGetCurrentOrderRound(VokoTestCase):
    def setUp(self):
        self.mock_datetime = self.patch("ordering.core.datetime")
        # Default return value
        self.mock_datetime.now.return_value = datetime.now(UTC)

    def test_given_no_order_rounds_function_returns_none(self):
        ret = get_current_order_round()
        self.assertIsNone(ret)

    def test_given_one_open_order_round_it_is_returned(self):
        self.mock_datetime.now.return_value = datetime(2014, 10, 28, 0, 0, tzinfo=UTC)
        orderround = OrderRoundFactory(
            open_for_orders=datetime(2014, 10, 27, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 10, 31, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 5, 17, 30, tzinfo=UTC)
        )
        ret = get_current_order_round()
        self.assertEqual(ret, orderround)

    def test_given_one_closed_order_round_it_is_returned(self):
        self.mock_datetime.now.return_value = datetime(2014, 11, 6, 0, 0, tzinfo=UTC)
        orderround = OrderRoundFactory(
            open_for_orders=datetime(2014, 10, 27, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 10, 31, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 5, 17, 30, tzinfo=UTC)
        )
        ret = get_current_order_round()
        self.assertEqual(ret, orderround)

    def test_given_a_previous_and_a_current_order_round_the_current_is_returned(self):
        previous = OrderRoundFactory(
            open_for_orders=datetime(2014, 10, 27, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 10, 31, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 5, 17, 30, tzinfo=UTC)
        )
        current = OrderRoundFactory(
            open_for_orders=datetime(2014, 11, 10, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 11, 14, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 19, 17, 30, tzinfo=UTC)
        )
        self.mock_datetime.now.return_value = datetime(2014, 11, 15, 0, 0, tzinfo=UTC)

        ret = get_current_order_round()
        self.assertEqual(ret, current)

    def test_given_a_current_and_a_future_order_round_the_current_is_returned(self):
        current = OrderRoundFactory(
            open_for_orders=datetime(2014, 10, 27, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 10, 31, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 5, 17, 30, tzinfo=UTC)
        )
        future = OrderRoundFactory(
            open_for_orders=datetime(2014, 11, 10, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 11, 14, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 19, 17, 30, tzinfo=UTC)
        )
        self.mock_datetime.now.return_value = datetime(2014, 11, 4, 0, 0, tzinfo=UTC)

        ret = get_current_order_round()
        self.assertEqual(ret, current)

    def test_given_a_previous_and_a_future_order_round_the_future_round_is_returned(self):
        previous = OrderRoundFactory(
            open_for_orders=datetime(2014, 10, 27, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 10, 31, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 5, 17, 30, tzinfo=UTC)
        )
        future = OrderRoundFactory(
            open_for_orders=datetime(2014, 11, 10, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 11, 14, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 19, 17, 30, tzinfo=UTC)
        )
        self.mock_datetime.now.return_value = datetime(2014, 11, 7, 0, 0, tzinfo=UTC)

        ret = get_current_order_round()
        self.assertEqual(ret, future)

    def test_given_multiple_future_rounds_the_first_one_is_returned(self):
        future3 = OrderRoundFactory(
            open_for_orders=datetime(2014, 12, 8, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 12, 12, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 12, 17, 17, 30, tzinfo=UTC)
        )

        future2 = OrderRoundFactory(
            open_for_orders=datetime(2014, 11, 24, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 11, 28, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 12, 3, 17, 30, tzinfo=UTC)
        )

        future1 = OrderRoundFactory(
            open_for_orders=datetime(2014, 11, 10, 0, 0, tzinfo=UTC),
            closed_for_orders=datetime(2014, 11, 14, 19, 0, tzinfo=UTC),
            collect_datetime=datetime(2014, 11, 19, 17, 30, tzinfo=UTC)
        )

        self.mock_datetime.now.return_value = datetime(2014, 11, 1, 0, 0, tzinfo=UTC)

        ret = get_current_order_round()
        self.assertEqual(ret, future1)

    def test_given_multiple_open_order_rounds_return_first_one(self):
        round1 = OrderRoundFactory()
        round2 = OrderRoundFactory()

        self.assertTrue(round1.is_open)
        self.assertEqual(get_current_order_round(), round1)


class TestUpdateOrderTotals(VokoTestCase):
    def setUp(self):
        self.round = OrderRoundFactory()
        self.order = OrderFactory(order_round=self.round)

    def test_that_sold_out_product_is_removed(self):
        product = ProductFactory(order_round=self.round, maximum_total_order=10)
        self.assertEqual(10, product.amount_available)

        order1 = OrderFactory(order_round=self.round, finalized=True, paid=True)
        order1_product = OrderProductFactory(order=order1, product=product, amount=10)

        self.assertEqual(10, product.amount_ordered)
        self.assertEqual(0, product.amount_available)

        order2 = OrderFactory(order_round=self.round)
        order2_product = OrderProductFactory(order=order2, amount=1)

        update_totals_for_products_with_max_order_amounts(order2)

        self.assertEqual(1, len(product.orderproducts.all()))

    def test_that_order_amount_is_decreased(self):
        # 10 available
        product = ProductFactory(order_round=self.round, maximum_total_order=10)
        self.assertEqual(10, product.amount_available)

        order1 = OrderFactory(order_round=self.round, finalized=True, paid=True)
        order1_product = OrderProductFactory(order=order1, product=product, amount=8)

        # 8 ordered, leaves 2
        self.assertEqual(8, product.amount_ordered)
        self.assertEqual(2, product.amount_available)

        # attempt to order 5
        order2 = OrderFactory(order_round=self.round)
        order2_product = OrderProductFactory(order=order2, product=product, amount=5)

        update_totals_for_products_with_max_order_amounts(order2)

        # re-fetch, amount is decreased to remaining 2
        order2_product = OrderProduct.objects.get(pk=order2_product.pk)
        self.assertEqual(2, order2_product.amount)

    def test_sold_out_stock_product_is_removed(self):
        # 10 available
        product = ProductFactory(order_round=None)
        ProductStockFactory(product=product, amount=10)
        self.assertEqual(10, product.amount_available)

        order1 = OrderFactory(order_round=self.round, finalized=True, paid=True)
        order1_product = OrderProductFactory(order=order1, product=product, amount=10)

        # 10 ordered, 0 remain
        self.assertEqual(10, product.amount_ordered)
        self.assertEqual(0, product.amount_available)

        # order 1 more
        order2 = OrderFactory(order_round=self.round)
        order2_product = OrderProductFactory(order=order2, product=product, amount=1)

        self.assertEqual(2, len(product.orderproducts.all()))
        update_totals_for_products_with_max_order_amounts(order2)
        self.assertEqual(1, len(product.orderproducts.all()))

    def test_that_stock_product_amount_is_decreased(self):
        # 10 available
        product = ProductFactory(order_round=None)
        ProductStockFactory(product=product, amount=10)
        self.assertEqual(10, product.amount_available)

        order1 = OrderFactory(order_round=self.round, finalized=True, paid=True)
        order1_product = OrderProductFactory(order=order1, product=product, amount=8)

        # 8 ordered, leaves 2
        self.assertEqual(8, product.amount_ordered)
        self.assertEqual(2, product.amount_available)

        # attempt to order 5
        order2 = OrderFactory(order_round=self.round)
        order2_product = OrderProductFactory(order=order2, product=product, amount=5)

        update_totals_for_products_with_max_order_amounts(order2)

        # re-fetch, amount is decreased to remaining 2
        order2_product = OrderProduct.objects.get(pk=order2_product.pk)
        self.assertEqual(2, order2_product.amount)
