from decimal import Decimal
import os
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from .models import CustomerProfile, MenuItem, Order, OrderItem, Restaurant

User = get_user_model()


class DineQuickPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testcustomer",
            email="testcustomer@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="Customer",
        )
        self.profile = CustomerProfile.objects.create(user=self.user, phone="+91 9999988888")

        self.restaurant = Restaurant.objects.create(name="Royal Feast", city="Mumbai")
        self.item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Paneer Tikka",
            price=Decimal("200.00"),
            category=MenuItem.Category.STARTER,
            available=True,
        )
        self.item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Biryani",
            price=Decimal("350.00"),
            category=MenuItem.Category.MAIN,
            available=True,
        )
        self.item_unavailable = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Unavailable Sweet",
            price=Decimal("100.00"),
            category=MenuItem.Category.DESSERT,
            available=False,
        )

    def test_unauthenticated_can_browse_restaurants_and_menus(self):
        """Visitors can view the restaurant list and restaurant menu without logging in."""
        res = self.client.get(reverse("restaurant-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Royal Feast")

        res_menu = self.client.get(reverse("restaurant-menu", kwargs={"pk": self.restaurant.pk}))
        self.assertEqual(res_menu.status_code, 200)
        self.assertContains(res_menu, "Paneer Tikka")
        self.assertContains(res_menu, "Biryani")
        # Unavailable items should not be displayed
        self.assertNotContains(res_menu, "Unavailable Sweet")

    def test_registration_creates_account_and_profile(self):
        """Registration view creates an active user with hashed password."""
        res = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "NewPassword123!",
                "password2": "NewPassword123!",
            },
        )
        self.assertEqual(res.status_code, 302)
        new_user = User.objects.get(username="newuser")
        self.assertTrue(new_user.check_password("NewPassword123!"))
        self.assertTrue(CustomerProfile.objects.filter(user=new_user).exists())

    def test_login_flow(self):
        """User can log in with username and password."""
        res = self.client.post(
            reverse("login"),
            {"username": "testcustomer", "password": "securepassword123"},
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_order_placement_requires_authentication(self):
        """Unauthenticated order attempts redirect to login."""
        res = self.client.post(
            reverse("place-order", kwargs={"pk": self.restaurant.pk}),
            {f"qty_{self.item1.pk}": 2},
        )
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)

    def test_successful_order_placement_and_billing(self):
        """Order placement creates Order, OrderItems, calculates bill in Python, sends email & logs."""
        self.client.login(username="testcustomer", password="securepassword123")
        mail.outbox.clear()

        log_path = Path(settings.BASE_DIR) / "orders_log.txt"
        if log_path.exists():
            log_path.unlink()

        res = self.client.post(
            reverse("place-order", kwargs={"pk": self.restaurant.pk}),
            {
                f"qty_{self.item1.pk}": 2,  # 2 * 200 = 400
                f"qty_{self.item2.pk}": 1,  # 1 * 350 = 350
            },
        )
        self.assertEqual(res.status_code, 302)

        order = Order.objects.latest("pk")
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.restaurant, self.restaurant)
        # Python calculated total: 400 + 350 = 750
        self.assertEqual(order.total, Decimal("750.00"))
        self.assertEqual(order.items.count(), 2)

        # Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(f"Order #{order.pk}", mail.outbox[0].subject)
        self.assertIn("750.00", mail.outbox[0].body)

        # Check file logging
        self.assertTrue(log_path.exists())
        content = log_path.read_text(encoding="utf-8")
        self.assertIn(f"order_id={order.pk}", content)
        self.assertIn("total=Rs 750.00", content)

    def test_profile_update_and_photo_upload(self):
        """Profile view updates names, phone, and uploads photo."""
        self.client.login(username="testcustomer", password="securepassword123")

        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04"
            b"\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44"
            b"\x01\x00\x3b"
        )
        uploaded_photo = SimpleUploadedFile("avatar.gif", small_gif, content_type="image/gif")

        res = self.client.post(
            reverse("profile"),
            {
                "first_name": "UpdatedName",
                "last_name": "UpdatedSurname",
                "phone": "+91 8888877777",
                "photo": uploaded_photo,
            },
        )
        self.assertEqual(res.status_code, 302)
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedName")
        self.assertEqual(self.user.last_name, "UpdatedSurname")
        self.assertEqual(self.profile.phone, "+91 8888877777")
        self.assertTrue(bool(self.profile.photo))

    def test_section_d_api_unauthenticated(self):
        """Section D API returns 403 JSON when not authenticated."""
        res = self.client.get(reverse("restaurant-menu-api", kwargs={"restaurant_id": self.restaurant.pk}))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json(), {"message": "Authentication required"})

    def test_section_d_api_restaurant_not_found(self):
        """Section D API returns 404 JSON for non-existent restaurant."""
        self.client.login(username="testcustomer", password="securepassword123")
        res = self.client.get(reverse("restaurant-menu-api", kwargs={"restaurant_id": 99999}))
        self.assertEqual(res.status_code, 404)
        self.assertIn("error", res.json())

    def test_section_d_api_filtering_and_validation(self):
        """Section D API filters available items and validates max_price."""
        self.client.login(username="testcustomer", password="securepassword123")

        # Without max_price: returns available items (200, 350)
        res = self.client.get(reverse("restaurant-menu-api", kwargs={"restaurant_id": self.restaurant.pk}))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 2)

        # With max_price=250: should return only item1 (200)
        res_filtered = self.client.get(
            reverse("restaurant-menu-api", kwargs={"restaurant_id": self.restaurant.pk}) + "?max_price=250"
        )
        self.assertEqual(res_filtered.status_code, 200)
        filtered_data = res_filtered.json()
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]["name"], "Paneer Tikka")

        # With invalid max_price: should return 400 JSON
        res_invalid = self.client.get(
            reverse("restaurant-menu-api", kwargs={"restaurant_id": self.restaurant.pk}) + "?max_price=invalid"
        )
        self.assertEqual(res_invalid.status_code, 400)
        self.assertIn("error", res_invalid.json())
