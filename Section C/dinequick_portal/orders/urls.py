from django.urls import path
from . import views

urlpatterns = [
    path("", views.restaurant_list, name="restaurant-list"),
    path("restaurants/<int:pk>/", views.restaurant_menu, name="restaurant-menu"),
    path("restaurants/<int:pk>/order/", views.place_order, name="place-order"),
    path("orders/<int:pk>/", views.order_detail, name="order-detail"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    # Section D AI view integration
    path("api/menu/<int:restaurant_id>/", views.restaurant_menu_api, name="restaurant-menu-api"),
]
