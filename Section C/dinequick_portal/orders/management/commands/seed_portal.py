from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from orders.models import Restaurant, MenuItem, CustomerProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the DineQuick portal with sample restaurants, menu items, and test users."

    def handle(self, *args, **options):
        self.stdout.write("Seeding DineQuick Food Ordering Portal data...")

        # 1. Create Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@dinequick.local",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin123)"))

        # 2. Create Demo Customer
        customer, created = User.objects.get_or_create(
            username="rahul_sharma",
            defaults={
                "email": "rahul.sharma@example.com",
                "first_name": "Rahul",
                "last_name": "Sharma",
            },
        )
        if created:
            customer.set_password("customer123")
            customer.save()
            profile, _ = CustomerProfile.objects.get_or_create(user=customer)
            profile.phone = "+91 9820012345"
            profile.save()
            self.stdout.write(self.style.SUCCESS("Created demo customer (rahul_sharma / customer123)"))

        # 3. Create Restaurants
        restaurants_data = [
            {"name": "Spice Route Bistro", "city": "Mumbai"},
            {"name": "The Royal Awadh", "city": "Delhi"},
            {"name": "Green Harvest Organics", "city": "Bengaluru"},
            {"name": "Coastal Treat Kitchen", "city": "Mumbai"},
        ]

        restaurants = {}
        for r_data in restaurants_data:
            rest, _ = Restaurant.objects.get_or_create(name=r_data["name"], defaults={"city": r_data["city"]})
            restaurants[r_data["name"]] = rest

        # 4. Create Menu Items
        menu_items_data = [
            # Spice Route Bistro (Mumbai)
            ("Paneer Tikka Angara", Decimal("260.00"), MenuItem.Category.STARTER, True, "Spice Route Bistro"),
            ("Corn Cheese Balls", Decimal("190.00"), MenuItem.Category.STARTER, True, "Spice Route Bistro"),
            ("Dal Makhani Royale", Decimal("290.00"), MenuItem.Category.MAIN, True, "Spice Route Bistro"),
            ("Hyderabadi Dum Biryani", Decimal("340.00"), MenuItem.Category.MAIN, True, "Spice Route Bistro"),
            ("Gulab Jamun with Rabdi", Decimal("120.00"), MenuItem.Category.DESSERT, True, "Spice Route Bistro"),
            ("Kesariya Masala Chai", Decimal("60.00"), MenuItem.Category.BEVERAGE, True, "Spice Route Bistro"),
            ("Fresh Mango Lassi", Decimal("95.00"), MenuItem.Category.BEVERAGE, True, "Spice Route Bistro"),

            # The Royal Awadh (Delhi)
            ("Galouti Kebab Platter", Decimal("320.00"), MenuItem.Category.STARTER, True, "The Royal Awadh"),
            ("Dahi Ke Kebab", Decimal("240.00"), MenuItem.Category.STARTER, True, "The Royal Awadh"),
            ("Awadhi Paneer Korma", Decimal("310.00"), MenuItem.Category.MAIN, True, "The Royal Awadh"),
            ("Lucknowi Biryani", Decimal("360.00"), MenuItem.Category.MAIN, True, "The Royal Awadh"),
            ("Shahi Tukda", Decimal("150.00"), MenuItem.Category.DESSERT, True, "The Royal Awadh"),
            ("Royal Rose Sharbat", Decimal("80.00"), MenuItem.Category.BEVERAGE, True, "The Royal Awadh"),

            # Green Harvest Organics (Bengaluru)
            ("Quinoa Avocado Salad", Decimal("240.00"), MenuItem.Category.STARTER, True, "Green Harvest Organics"),
            ("Mediterranean Hummus & Pita", Decimal("210.00"), MenuItem.Category.STARTER, True, "Green Harvest Organics"),
            ("Wild Mushroom Risotto", Decimal("380.00"), MenuItem.Category.MAIN, True, "Green Harvest Organics"),
            ("Vegan Buddha Bowl", Decimal("320.00"), MenuItem.Category.MAIN, True, "Green Harvest Organics"),
            ("Chia Seed Berry Pudding", Decimal("160.00"), MenuItem.Category.DESSERT, True, "Green Harvest Organics"),
            ("Cold-Pressed Green Juice", Decimal("130.00"), MenuItem.Category.BEVERAGE, True, "Green Harvest Organics"),

            # Coastal Treat Kitchen (Mumbai)
            ("Crispy Bombil Fry", Decimal("280.00"), MenuItem.Category.STARTER, True, "Coastal Treat Kitchen"),
            ("Prawn Gassi with Appam", Decimal("420.00"), MenuItem.Category.MAIN, True, "Coastal Treat Kitchen"),
            ("Steamed Fish Curry", Decimal("390.00"), MenuItem.Category.MAIN, True, "Coastal Treat Kitchen"),
            ("Sol Kadhi", Decimal("70.00"), MenuItem.Category.BEVERAGE, True, "Coastal Treat Kitchen"),
            ("Caramel Custard", Decimal("140.00"), MenuItem.Category.DESSERT, True, "Coastal Treat Kitchen"),
        ]

        count = 0
        for name, price, category, available, r_name in menu_items_data:
            _, created = MenuItem.objects.get_or_create(
                name=name,
                restaurant=restaurants[r_name],
                defaults={
                    "price": price,
                    "category": category,
                    "available": available,
                },
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(restaurants)} restaurants and {count} menu items!"))
