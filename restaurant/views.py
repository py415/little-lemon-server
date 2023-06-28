from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer, UserSerializer


# Create your views here.
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class BookingView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all the bookings for the currently authenticated user.

        Returns empty list if user is anonymous.
        """
        user = self.request.user

        if not user.is_anonymous:
            return Booking.objects.filter(user=user)

        return Booking.objects.none()


class MenuItemView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser]
