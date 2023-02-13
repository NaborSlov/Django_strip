from django.urls import path

from strip.views import BuyView, GetItemView

urlpatterns = [
    path('buy/<int:id>', BuyView.as_view()),
    path('order/<int:id>', GetItemView.as_view()),
]
