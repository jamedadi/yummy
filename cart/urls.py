from django.urls import path

from .views import AddToCartView

app_name = 'cart'

urlpatterns = [
    path('addtocart/<int:item_pk>/', AddToCartView.as_view(), name='add-to-cart'),
]