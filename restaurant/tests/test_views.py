import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Menu


class ViewsTest(TestCase):
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

        # Create mock menu item
        self.menu_item = Menu.objects.create(title="Ice Cream", price=80, inventory=100)

        # Create mock menu item data
        self.menu_item_data = {
            "title": "Hamburgers",
            "price": 90.95,
            "inventory": 200,
        }

        # Create mock booking data
        booking_date = datetime.datetime.now()
        self.mock_booking_data = {
            "user": self.test_user.id,
            "name": "Philip",
            "no_of_guests": 3,
            "booking_date": booking_date.isoformat(),
            "booking_time": booking_date.time().isoformat(),
            "occasion": "Birthday",
        }

    def test_get_all_menu_items_unauthenticated(self):
        url = reverse("menu")
        response = self.unauthenticated_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_menu_item_unauthenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.unauthenticated_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Ice Cream")
        self.assertEqual(response.data["price"], "80.00")
        self.assertEqual(response.data["inventory"], 100)

    def test_get_all_bookings_unauthenticated(self):
        url = reverse("bookings")
        response = self.unauthenticated_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_menu_items_authenticated(self):
        url = reverse("menu")
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_menu_item_authenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Ice Cream")
        self.assertEqual(response.data["price"], "80.00")
        self.assertEqual(response.data["inventory"], 100)

    def test_get_all_bookings_authenticated(self):
        url = reverse("bookings")
        response = self.authenticated_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_menu_item_unauthenticated(self):
        url = reverse("menu")
        response = self.unauthenticated_client.post(url, data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking_unauthenticated(self):
        url = reverse("bookings")
        response = self.unauthenticated_client.post(url, data=self.mock_booking_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_authenticated(self):
        url = reverse("menu")
        response = self.authenticated_client.post(url, data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_authenticated_authorized(self):
        self.test_user.is_staff = True
        self.test_user.save()
        url = reverse("menu")
        response = self.authenticated_client.post(url, data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.menu_item_data["title"])
        self.assertEqual(response.data["price"], str(self.menu_item_data["price"]))
        self.assertEqual(response.data["inventory"], self.menu_item_data["inventory"])

    def test_create_booking_authenticated(self):
        url = reverse("bookings")
        response = self.authenticated_client.post(url, data=self.mock_booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.mock_booking_data["name"])
        self.assertEqual(
            response.data["no_of_guests"], self.mock_booking_data["no_of_guests"]
        )
        self.assertEqual(
            response.data["booking_date"], self.mock_booking_data["booking_date"] + "Z"
        )
        self.assertEqual(
            response.data["booking_time"], self.mock_booking_data["booking_time"]
        )
        self.assertEqual(response.data["occasion"], self.mock_booking_data["occasion"])

    def test_update_menu_item_unauthenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.unauthenticated_client.put(url, data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_menu_item_authenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.put(url, data=self.menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_menu_item_authenticated_authorized(self):
        self.test_user.is_staff = True
        self.test_user.save()
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.put(
            url, data=self.menu_item_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.menu_item_data["title"])
        self.assertEqual(response.data["price"], str(self.menu_item_data["price"]))
        self.assertEqual(response.data["inventory"], self.menu_item_data["inventory"])

    def test_delete_menu_item_unauthenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.unauthenticated_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_menu_item_authenticated(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_menu_item_authenticated_authorized(self):
        self.test_user.is_staff = True
        self.test_user.save()
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_menu_item_expected_fields(self):
        url = reverse("menu_item", kwargs={"pk": self.menu_item.id})
        response = self.authenticated_client.get(url)
        self.assertEqual(
            set(response.data.keys()), {"id", "title", "price", "inventory"}
        )
