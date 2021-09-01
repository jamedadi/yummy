from django.urls import path

from .views import ServiceCreateView, ServiceUpdateView, ServiceDeleteView, ServiceDetailView, ServiceListView, \
    ServiceCategoryCreateView, ServiceCategoryUpdateView, ServiceCategoryDeleteView, ServiceCategoryDetailView, \
    DeliveryAreaCreate, DeliveryUpdateView

app_name = 'service'

urlpatterns = (
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('update/<int:pk>', ServiceUpdateView.as_view(), name='service-update'),
    path('delete/<int:pk>', ServiceDeleteView.as_view(), name='service-delete'),
    path('detail/<int:pk>', ServiceDetailView.as_view(), name='service-detail'),
    path('list/', ServiceListView.as_view(), name='service-list'),

    path('category/create/<int:service_pk>/', ServiceCategoryCreateView.as_view(), name='service-category-create'),
    path('category/update/<int:pk>/', ServiceCategoryUpdateView.as_view(), name='service-category-update'),
    path('category/delete/<int:pk>/', ServiceCategoryDeleteView.as_view(), name='service-category-delete'),
    path('category/detail/<int:pk>', ServiceCategoryDetailView.as_view(), name='service-category-detail'),

    path('deliveryarea/create/<int:service_pk>', DeliveryAreaCreate.as_view(), name='delivery-area-create'),
    path('deliveryarea/update/<int:pk>', DeliveryUpdateView.as_view(), name='delivery-area-update'),
)
