from django.urls import path

from .views import OrdersList, Checkout

urlpatterns = [
    path("checkout/", Checkout.as_view()),
    path("orders/", OrdersList.as_view()),
]
