from django.db import models
class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self): return self.name
class MenuItem(models.Model):
    class Category(models.TextChoices):
        STARTER = "Starter", "Starter"
        MAIN = "Main", "Main"
        DESSERT = "Dessert", "Dessert"
        BEVERAGE = "Beverage", "Beverage"
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=10, choices=Category.choices)
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    def __str__(self): return self.name
