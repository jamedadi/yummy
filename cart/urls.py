from django.urls import path

from cart.views import AddToCartView, CartLineDeleteView, CartLineDecreaseView, EmptyCartView

app_name = 'cart'

urlpatterns = [
    path('addtocart/<int:item_pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cartline/delete/<int:pk>/', CartLineDeleteView.as_view(), name='cart-line-delete'),
    path('cartline/decrease/<int:pk>/', CartLineDecreaseView.as_view(), name='cart-line-decrease'),
    path('cart-empty/<int:pk>/', EmptyCartView.as_view(), name='empty-cart'),

]
