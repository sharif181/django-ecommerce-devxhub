# urls.py
from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    OrderView,
    ProductDetailView,
    ProductListView,
    ProfileView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('profile/', ProfileView.as_view(), name='api-profile'),
    path('products/', ProductListView.as_view(), name='api-product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='api-product_detail'),
    path('orders/', OrderView.as_view(), name='api-order_list'),
]
