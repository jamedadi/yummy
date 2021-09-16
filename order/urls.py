from django.urls import path

from order.views import OrderServiceListView, OrderServiceDetailView, OrderServiceUpdateView, OrderServiceListFilterView
from order.views import CustomerOrdersListView, CustomerOrderDetailView

app_name = 'order'

urlpatterns = [
    path('service/list/<int:service_pk>/', OrderServiceListFilterView.as_view(), name='service-order-list'),
    path('service/today/<int:service_pk>/', OrderServiceListView.as_view(), name='service-order-today'),
    path('service/detail/<int:pk>/', OrderServiceDetailView.as_view(), name='service-order-detail'),
    path('service/update/<int:pk>/', OrderServiceUpdateView.as_view(), name='service-order-update'),
  
    path('customer/list/', CustomerOrdersListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/detail/', CustomerOrderDetailView.as_view(), name='customer-detail'),
]