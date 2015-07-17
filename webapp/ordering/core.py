from pytz import UTC
import models
from datetime import datetime


def get_current_order_round():
    """
    Return the current order round.
    If there's no current order round, return the next one.
    If there's not current or next order round, return the previous one.
    If there's no order round at all, return None.

    :return: OrderRound object || None
    """
    now = datetime.now(UTC)
    order_rounds = models.OrderRound.objects.all()

    # No rounds at all (empty DB)
    if order_rounds.count() == 0:
        return

    # Exact match to open round
    filtered = order_rounds.filter(open_for_orders__lte=now,
                                   collect_datetime__gt=now)
    if filtered.count() == 1:
        return filtered.get()

    # Future round(s)
    filtered = order_rounds.filter(open_for_orders__gte=now)
    if filtered.count() > 0:
        return filtered.order_by("open_for_orders")[0]

    # Previous round(s)
    filtered = order_rounds.filter(collect_datetime__lt=now)
    if filtered.count() > 0:
        return filtered.order_by("-open_for_orders")[0]


def get_or_create_order(user):
    try:
        return models.Order.objects.get_or_create(paid=False,
                                                  user=user,
                                                  order_round=get_current_order_round())[0]
    except IndexError:
        raise RuntimeError("Nog geen bestelronde aangemaakt!")


def get_order_product(product, order):
    existing_ops = models.OrderProduct.objects.filter(product=product, order=order)
    if existing_ops:
        return existing_ops[0]


def update_totals_for_products_with_max_order_amounts(order):
    ### TODO: Add messages about deleted / changed orderproducts
    for orderproduct in order.orderproducts.all().exclude(product__maximum_total_order__exact=None):
        if orderproduct.amount > orderproduct.product.amount_available:
            if orderproduct.product.amount_available > 0:
                orderproduct.amount = orderproduct.product.amount_available
                orderproduct.save()

            else:
                orderproduct.delete()