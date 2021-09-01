from django.urls import path
from item.views import ItemUpdateView

app_name = 'item'

urlpatterns = [
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
]
