from django.urls import path

from .views import ServiceProviderServiceCreateView, ServiceProviderServiceUpdateView, ServiceProviderServiceDeleteView, \
    ServiceProviderServiceDetailView, ServiceProviderServiceListView, ServiceProviderServiceCategoryCreateView, \
    ServiceProviderServiceCategoryUpdateView, ServiceProviderServiceCategoryDeleteView, \
    ServiceProviderDeliveryAreaCreate, ServiceProviderDeliveryUpdateView, \
    ServiceProviderDeliveryDeleteView, ServiceProviderServiceAvailableTimeCreateView, \
    ServiceProviderServiceAvailableTimeUpdateView, ServiceProviderServiceAvailableTimeDeleteView, ServiceListView

app_name = 'service'

urlpatterns = (
    path('serviceprovider/create/', ServiceProviderServiceCreateView.as_view(),
         name='service-provider-service-create'),
    path('serviceprovider/update/<int:pk>', ServiceProviderServiceUpdateView.as_view(),
         name='service-provider-service-update'),
    path('serviceprovider/delete/<int:pk>', ServiceProviderServiceDeleteView.as_view(),
         name='service-provider-service-delete'),
    path('serviceprovider/detail/<int:pk>', ServiceProviderServiceDetailView.as_view(),
         name='service-provider-service-detail'),
    path('serviceprovider/list/', ServiceProviderServiceListView.as_view(), name='service-provider-service-list'),

    path('serviceprovider/category/create/<int:service_pk>/', ServiceProviderServiceCategoryCreateView.as_view(),
         name='service-provider-service-category-create'),
    path('serviceprovider/category/update/<int:pk>/', ServiceProviderServiceCategoryUpdateView.as_view(),
         name='service-provider-service-category-update'),
    path('serviceprovider/category/delete/<int:pk>/', ServiceProviderServiceCategoryDeleteView.as_view(),
         name='service-provider-service-category-delete'),

    path('serviceprovider/deliveryarea/create/<int:service_pk>', ServiceProviderDeliveryAreaCreate.as_view(),
         name='service-provider-delivery-area-create'),
    path('serviceprovider/deliveryarea/update/<int:pk>', ServiceProviderDeliveryUpdateView.as_view(),
         name='service-provider-delivery-area-update'),
    path('serviceprovider/deliveryarea/delete/<int:pk>', ServiceProviderDeliveryDeleteView.as_view(),
         name='service-provider-delivery-area-delete'),

    path(
        'serviceprovider/availabletime/create/<int:service_pk>',
        ServiceProviderServiceAvailableTimeCreateView.as_view(),
        name='service-provider-available-time-create'
    ),
    path('serviceprovider/availabletime/update/<int:pk>', ServiceProviderServiceAvailableTimeUpdateView.as_view(),
         name='service-provider-available-time-update'),
    path('serviceprovider/availabletime/delete/<int:pk>', ServiceProviderServiceAvailableTimeDeleteView.as_view(),
         name='service-provider-available-time-delete'),

    path('list/', ServiceListView.as_view(), name='service-list')
)
