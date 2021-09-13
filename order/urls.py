from django.urls import path

from order.views import CustomerOrdersListView, CustomerOrderDetailView

app_name = 'order'

urlpatterns = [
    path('customer/list/', CustomerOrdersListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/detail/', CustomerOrderDetailView.as_view(), name='customer-detail'),
]