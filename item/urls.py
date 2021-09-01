from django.urls import path
from item.views import ItemUpdateView, ItemDetailView, ItemDeleteView

app_name = 'item'

urlpatterns = [
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='detail'),

]
