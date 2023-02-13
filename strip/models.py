import stripe
from django.db import models


class Item(models.Model):
    class CurrencyChoice(models.TextChoices):
        RUB = 'rub'
        USD = 'usd'

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000000, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices, default=CurrencyChoice.RUB)

    @property
    def get_price(self):
        return int(self.price * 100)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.ForeignKey("Discount", on_delete=models.PROTECT)
    tax = models.ForeignKey("Tax", on_delete=models.PROTECT)
    items = models.ManyToManyField("Item")

    @property
    def total_price(self):
        return sum([item.price for item in self.items.all()])

    def __str__(self):
        return self.name


class Discount(models.Model):
    class Duration(models.TextChoices):
        ONCE = 'once'
        FOREVER = 'forever'
        REPEATING = 'repeating'

    id = models.CharField(max_length=80, primary_key=True)
    percent_off = models.IntegerField()
    duration = models.CharField(max_length=25, choices=Duration.choices, default=Duration.ONCE)
    created = models.BooleanField(default=False)

    def create_discount(self):
        stripe.Coupon.create(id=self.id,
                             percent_off=self.percent_off,
                             duration=self.duration)
        self.created = True
        self.save()


class Tax(models.Model):
    class DisplName(models.TextChoices):
        SALES_TAX = 'Sales Tax'
        VAT = "VAT"
        GST = "GST"

    id_tax = models.CharField(max_length=80, unique=True, blank=True, null=True)
    display_name = models.CharField(max_length=12, choices=DisplName.choices, default=DisplName.SALES_TAX)
    inclusive = models.BooleanField(default=False)
    percentage = models.FloatField()
    created = models.BooleanField(default=False)

    def create_tax(self):
        tax_new = stripe.TaxRate.create(display_name=self.display_name,
                                        inclusive=self.inclusive,
                                        percentage=self.percentage)
        self.id_tax = tax_new.id
        self.created = True
        self.save()
