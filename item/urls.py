from django.urls import path
from item.views import ItemUpdateView, ItemDetailView, ItemDeleteView, ServiceProviderItemDetailView, ItemCreateView, \
    ItemListView, ServiceCategoryItemListView

app_name = 'item'

urlpatterns = [
    path('create/<int:service_pk>/<int:category_pk>/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('detail-serviceprovider/<int:pk>/', ServiceProviderItemDetailView.as_view(), name='detail-service-provider'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('<int:service_pk>/list/', ItemListView.as_view(), name='list'),
    path(
        'serviceprovider/<int:service_pk>/<int:category_pk>/list/', ServiceCategoryItemListView.as_view(),
        name='service-provider-list'),
]
