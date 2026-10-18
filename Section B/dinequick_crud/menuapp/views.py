from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MenuItemForm
from .models import MenuItem, Restaurant

class MenuItemListView(ListView):
    model = MenuItem
    template_name = "menuapp/menuitem_list.html"
    context_object_name = "items"
    queryset = MenuItem.objects.select_related("restaurant").order_by("name")

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menuapp/menuitem_create.html"
    success_url = reverse_lazy("menu-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_restaurants"] = Restaurant.objects.exists()
        return context

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menuapp/menuitem_update.html"
    success_url = reverse_lazy("menu-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_restaurants"] = Restaurant.objects.exists()
        return context

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "menuapp/menuitem_confirm_delete.html"
    success_url = reverse_lazy("menu-list")
