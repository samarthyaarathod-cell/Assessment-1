from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import MenuItem, Restaurant

User = get_user_model()


class MenuItemCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(name="Taj Dining")
        self.menu_item = MenuItem.objects.create(
            name="Garlic Naan",
            price=Decimal("60.00"),
            category=MenuItem.Category.MAIN,
            available=True,
            restaurant=self.restaurant,
        )

    def test_menu_list_view_accessible_by_anyone(self):
        """ListView should be publicly accessible without login."""
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Garlic Naan")

    def test_create_view_requires_login(self):
        """CreateView must redirect unauthenticated users to the login page."""
        response = self.client.get(reverse("menu-add"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_view_authenticated(self):
        """CreateView allows authenticated users to create a menu item."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("menu-add"),
            {
                "name": "Butter Chicken",
                "price": "350.00",
                "category": "Main",
                "available": "on",
                "restaurant": self.restaurant.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuItem.objects.filter(name="Butter Chicken").exists())

    def test_update_view_requires_login(self):
        """UpdateView must redirect unauthenticated users to login."""
        response = self.client.get(reverse("menu-edit", kwargs={"pk": self.menu_item.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_view_authenticated(self):
        """UpdateView updates the item successfully."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("menu-edit", kwargs={"pk": self.menu_item.pk}),
            {
                "name": "Garlic Butter Naan",
                "price": "75.00",
                "category": "Main",
                "available": "on",
                "restaurant": self.restaurant.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, "Garlic Butter Naan")
        self.assertEqual(self.menu_item.price, Decimal("75.00"))

    def test_delete_view_requires_login(self):
        """DeleteView must redirect unauthenticated users to login."""
        response = self.client.get(reverse("menu-delete", kwargs={"pk": self.menu_item.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_view_authenticated(self):
        """DeleteView deletes the item for an authenticated user."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("menu-delete", kwargs={"pk": self.menu_item.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())
