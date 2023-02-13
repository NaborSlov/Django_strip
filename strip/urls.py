from django.urls import path

from strip.views import BuyView, GetItemView

urlpatterns = [
    path('buy/<int:id>', BuyView.as_view(), name="buy"),
    path('order/<int:id>', GetItemView.as_view(), name="order"),
]
