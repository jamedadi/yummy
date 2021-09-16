from django.urls import path

from cart.views import AddToCartView, CartLineDeleteView, CartLineDecreaseView, EmptyCartView

app_name = 'cart'

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cartline/delete/<int:pk>/', CartLineDeleteView.as_view(), name='cart-line-delete'),
    path('cartline/decrease/<int:pk>/', CartLineDecreaseView.as_view(), name='cart-line-decrease'),
    path('cart-empty/', EmptyCartView.as_view(), name='empty-cart'),

]
