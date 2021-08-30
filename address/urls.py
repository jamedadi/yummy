from django.urls import path

from .views import CustomerAddressCreateView

app_name = 'address'

urlpatterns = [
    path('customer/create', CustomerAddressCreateView.as_view(), name='customer-address-create')
]
