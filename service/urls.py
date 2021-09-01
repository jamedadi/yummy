from django.urls import path

from .views import ServiceCreateView, ServiceListView

app_name = 'service'

urlpatterns = (
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('list/', ServiceListView.as_view(), name='service-list'),
)
