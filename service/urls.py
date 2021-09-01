from django.urls import path

from .views import ServiceCreateView, ServiceUpdateView, ServiceDeleteView, ServiceListView

app_name = 'service'

urlpatterns = (
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('update/<int:pk>', ServiceUpdateView.as_view(), name='service-update'),
    path('delete/<int:pk>', ServiceDeleteView.as_view(), name='service-delete'),
    path('list/', ServiceListView.as_view(), name='service-list'),
)
