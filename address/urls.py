from django.urls import path

from .views import CustomerAddressCreateView, CustomerAddressUpdateView, CustomerAddressDeleteView, \
    ServiceAddressCreateView

app_name = 'address'

urlpatterns = [
    path('customer/create', CustomerAddressCreateView.as_view(), name='customer-address-create'),
    path('customer/update/<int:pk>', CustomerAddressUpdateView.as_view(), name='customer-address-update'),
    path('customer/delete/<int:pk>', CustomerAddressDeleteView.as_view(), name='customer-address-delete'),
    path('service/create/<int:service_pk>/', ServiceAddressCreateView.as_view(), name='service-address-delete'),
]
