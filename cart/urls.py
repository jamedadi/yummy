from django.urls import path

from .views import AddToCartView, CartLineDeleteView

app_name = 'cart'

urlpatterns = [
    path('addtocart/<int:item_pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cartline/delete/<int:pk>/', CartLineDeleteView.as_view(), name='cart-line-delete'),
]
