from django.urls import path

from .views import ServiceCreateView, ServiceUpdateView, ServiceListView

app_name = 'service'

urlpatterns = (
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('update/<int:pk>', ServiceUpdateView.as_view(), name='service-update'),
    path('list/', ServiceListView.as_view(), name='service-list'),
)
