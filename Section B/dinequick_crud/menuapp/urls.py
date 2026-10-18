from django.urls import path
from .views import MenuItemListView, MenuItemCreateView, MenuItemUpdateView, MenuItemDeleteView
urlpatterns = [path("menu/", MenuItemListView.as_view(), name="menu-list"), path("menu/add/", MenuItemCreateView.as_view(), name="menu-add"), path("menu/<int:pk>/edit/", MenuItemUpdateView.as_view(), name="menu-edit"), path("menu/<int:pk>/delete/", MenuItemDeleteView.as_view(), name="menu-delete")]
