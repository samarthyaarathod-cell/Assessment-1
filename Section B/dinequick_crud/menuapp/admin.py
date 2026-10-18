from django.contrib import admin
from .models import MenuItem, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "category", "price", "available")
    list_filter = ("category", "available", "restaurant")
    search_fields = ("name", "restaurant__name")
    list_editable = ("price", "available")
