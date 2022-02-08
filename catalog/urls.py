from django.urls import path

from .views import BicycleDetailAPI, BicycleListAPI, OrderCreateAPI, OrderListAPI

urlpatterns = [
    path('list/', BicycleListAPI.as_view(), name='bicycle-list'),
    path('list/<int:pk>/', BicycleDetailAPI.as_view(), name='bicycle-detail'),
    path('order/list/', OrderListAPI.as_view(), name='order-list'),
    path('order/create/', OrderCreateAPI.as_view(), name='order-create'),
]
