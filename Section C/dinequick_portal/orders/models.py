from django.conf import settings
from django.db import models
class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100)
    def __str__(self): return self.name
class MenuItem(models.Model):
    class Category(models.TextChoices):
        STARTER = "Starter", "Starter"
        MAIN = "Main", "Main"
        DESSERT = "Dessert", "Dessert"
        BEVERAGE = "Beverage", "Beverage"
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=10, choices=Category.choices)
    available = models.BooleanField(default=True)
    def __str__(self): return f"{self.name} ({self.restaurant})"
class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "Placed", "Placed"
        PREPARING = "Preparing", "Preparing"
        OUT = "Out for delivery", "Out for delivery"
        DELIVERED = "Delivered", "Delivered"
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    placed_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name="order_lines")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    @property
    def line_total(self): return self.quantity * self.unit_price
class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True)
