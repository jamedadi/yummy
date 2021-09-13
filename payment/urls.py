from django.urls import path

from payment.views import CheckoutView

app_name = 'payment'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
