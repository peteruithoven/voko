from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel


class Payment(TimeStampedModel):
    """ Payment by a user  """
    # TODO link to balance model
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey("ordering.Order", null=True, related_name="payments")

    transaction_id = models.IntegerField()
    transaction_code = models.CharField(max_length=255)
    succeeded = models.BooleanField(default=False)

    def create_credit(self):
        return Balance.objects.create(user=self.order.user,
                                      type="CR",
                                      amount=self.amount,
                                      notes="iDeal betaling voor bestelling #%d" % self.order.pk)

    def __unicode__(self):
        status = "Succeeded" if self.succeeded else "Failed"
        return "%s payment of E%s by %s" % (status, self.amount, self.order.user)


class BalanceManager(models.Manager):
    use_for_related_fields = True

    def _credit(self):
        credit_objs = self.get_queryset().filter(type="CR")
        debit_objs = self.get_queryset().filter(type="DR")
        credit_sum = sum([b.amount for b in credit_objs])
        debit_sum = sum([b.amount for b in debit_objs])

        return credit_sum - debit_sum

    def _debit(self):
        return -self._credit()

    def credit(self):
        _credit = self._credit()
        return _credit if _credit > 0 else 0

    def debit(self):
        _debit = self._debit()
        return _debit if _debit > 0 else 0


class Balance(TimeStampedModel):
    """ User Balance. Should be renamed to UserBalance (TODO) """
    # TODO: add sanity check; amount may never be negative.
    TYPES = (
        ("CR", "Credit"),
        ("DR", "Debit"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="balance")
    type = models.CharField(max_length=2, choices=TYPES)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField()

    def __unicode__(self):
        return u"[%s] %s: %s" % (self.user, self.type, self.amount)

    objects = BalanceManager()


class VokoBalanceBase(TimeStampedModel):
    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = ""

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    order_round = models.ForeignKey("ordering.OrderRound", null=True, blank=True,
                                    related_name=Meta.verbose_name_plural.lower(),
                                    help_text="Optionally link to order round")

    supplier = models.ForeignKey("ordering.Supplier", null=True, blank=True,
                                 related_name=Meta.verbose_name_plural.lower(),
                                 help_text="Optionally link to supplier")

    user_balance = models.OneToOneField(Balance, null=True, blank=True,
                                        related_name=Meta.verbose_name.lower(),
                                        help_text="User balance, if any")

    def __unicode__(self):
        return str(self.amount)


class VokoIncome(VokoBalanceBase):
    class Meta:
        verbose_name = "Inkomste"
        verbose_name_plural = "Inkomsten"


class VokoExpense(VokoBalanceBase):
    class Meta:
        verbose_name = "Uitgave"
        verbose_name_plural = "Uitgaven"

