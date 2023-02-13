import stripe
from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import FieldDoesNotExist, ValidationError

from strip.models import Item, Order


class BuyView(View):
    def get(self, request, *args, **kwargs):
        id_buy = kwargs.get("id")
        try:
            order = Order.objects.select_related('discount', 'tax').prefetch_related('items').get(id=id_buy)
        except Item.DoesNotExist:
            raise FieldDoesNotExist

        if not order.discount.created:
            order.discount.create_discount()

        if not order.tax.created:
            order.tax.create_tax()

        if len(set(map(lambda x: x.currency, order.items.all()))) != 1:
            raise ValidationError("Валюта должна быть одного типа")

        items = []
        for item in order.items.all():
            items.append({
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name
                    },
                    'unit_amount': item.get_price,
                },
                'quantity': 1,
                'tax_rates': [order.tax.id_tax]
            })

        session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            discounts=[{
               'coupon': order.discount.id
            }],
            success_url='https://stripe.stripe.com/',
            cancel_url='https://stripe.stripe.com/',
        )

        return redirect(session.url)


class GetItemView(View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.prefetch_related('items').get(id=kwargs.get('id'))
        except Order.DoesNotExist:
            raise FieldDoesNotExist

        context = {'id': order.id,
                   'title': order.name,
                   'description': order.description,
                   'price': order.total_price}

        return render(request, 'buy/item.html', context=context, status=200)
