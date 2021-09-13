from django.urls import path

from payment.views import CheckoutView, PaymentVerify

app_name = 'payment'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('verify/', PaymentVerify.as_view(), name='verify'),
]
