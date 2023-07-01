from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("menu/", views.MenuItemView.as_view(), name="menu"),
    path("menu/<int:pk>", views.SingleMenuItemView.as_view(), name="menu_item"),
    path("bookings/", views.BookingView.as_view(), name="bookings"),
    path("bookings/<int:pk>", views.SingleBookingView.as_view(), name="booking_item"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
