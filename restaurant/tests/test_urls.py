from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import resolve, reverse

from ..models import Menu
from ..views import BookingView, MenuItemView, SingleMenuItemView


class UrlsTest(TestCase):
    def setUp(self):
        # Create an authenticated client
        test_user = {
            "username": "testuser",
            "password": "testpassword",
        }

        self.authenticated_client = Client()
        self.test_user = User.objects.create_user(
            username=test_user["username"], password=test_user["password"]
        )
        self.authenticated_client.login(
            username=test_user["username"], password=test_user["password"]
        )

        # Create an unauthenticated client
        self.unauthenticated_client = Client()

        # Create menu item
        self.test_menu_item = Menu.objects.create(
            title="Ice Cream", price=80, inventory=100
        )

    def test_menu_url(self):
        url = reverse("menu")
        self.assertEqual(resolve(url).func.view_class, MenuItemView)

    def test_menu_item_url(self):
        url = reverse("menu_item", args=[1])
        self.assertEqual(resolve(url).func.view_class, SingleMenuItemView)

    def test_bookings_url(self):
        url = reverse("bookings")
        self.assertEqual(resolve(url).func.view_class, BookingView)

    def test_menu_page_unauthenticated(self):
        response = self.unauthenticated_client.get("/api/menu/")
        self.assertEquals(response.status_code, 200)

    def test_menu_item_page_unauthenticated(self):
        url = reverse("menu_item", args=[self.test_menu_item.id])
        response = self.unauthenticated_client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_bookings_page_unauthenticated(self):
        response = self.unauthenticated_client.get("/api/bookings/")
        self.assertEquals(response.status_code, 403)

    def test_menu_page_authenticated(self):
        response = self.authenticated_client.get("/api/menu/")
        self.assertEquals(response.status_code, 200)

    def test_menu_item_page_authenticated(self):
        url = reverse("menu_item", args=[self.test_menu_item.id])
        response = self.authenticated_client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_bookings_page_authenticated(self):
        response = self.authenticated_client.get("/api/bookings/")
        self.assertEquals(response.status_code, 200)
