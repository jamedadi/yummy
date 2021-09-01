from django.urls import path

from .views import ServiceCreateView

app_name = 'service'

urlpatterns = (
    path('create/', ServiceCreateView.as_view(), name='service-create'),
)
