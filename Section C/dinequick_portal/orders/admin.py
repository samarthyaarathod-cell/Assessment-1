from django.contrib import admin
from .models import CustomerProfile, MenuItem, Order, OrderItem, Restaurant


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price", "line_total")


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city")
    search_fields = ("name", "city")
    list_filter = ("city",)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "category", "price", "available")
    search_fields = ("name", "restaurant__name")
    list_filter = ("category", "available", "restaurant__city")
    list_editable = ("price", "available")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "restaurant", "status", "total", "placed_at")
    search_fields = ("customer__username", "customer__email", "restaurant__name")
    list_filter = ("status", "placed_at", "restaurant")
    list_editable = ("status",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "menu_item", "quantity", "unit_price", "line_total")
    search_fields = ("menu_item__name", "order__id", "order__customer__username")
    list_filter = ("menu_item__category",)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "photo")
    search_fields = ("user__username", "user__email", "phone")
    list_filter = ("user__is_active", "user__date_joined")
