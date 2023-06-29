import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase

from ..models import Booking, Menu


class ModelsTest(TestCase):
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

        # Create mock menu item data
        self.menu_item_data = {
            "title": "Hamburgers",
            "price": 90.95,
            "inventory": 200,
        }

        # Create mock booking data
        booking_date = datetime.datetime.now()
        self.mock_booking_data = {
            "user": self.test_user,
            "name": "Philip",
            "no_of_guests": 3,
            "booking_date": booking_date,
            "booking_time": booking_date.time(),
            "occasion": "Birthday",
        }

    def test_menu_item_creation(self):
        instance = Menu.objects.create(
            title=self.menu_item_data["title"],
            price=self.menu_item_data["price"],
            inventory=self.menu_item_data["inventory"],
        )
        self.assertIsNotNone(Menu.objects.get(id=instance.id))

    def test_booking_creation(self):
        instance = Booking.objects.create(
            user=self.mock_booking_data["user"],
            name=self.mock_booking_data["name"],
            no_of_guests=self.mock_booking_data["no_of_guests"],
            booking_date=self.mock_booking_data["booking_date"],
            booking_time=self.mock_booking_data["booking_time"],
            occasion=self.mock_booking_data["occasion"],
        )
        self.assertIsNotNone(Booking.objects.get(id=instance.id))
