from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "price", "category", "available", "restaurant"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "field-control", "placeholder": "e.g. Paneer Tikka"}),
            "price": forms.NumberInput(attrs={"class": "field-control", "placeholder": "0.00", "min": "0", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "field-control"}),
            "available": forms.CheckboxInput(attrs={"class": "field-checkbox"}),
            "restaurant": forms.Select(attrs={"class": "field-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        restaurants = self.fields["restaurant"].queryset.order_by("name")
        self.fields["restaurant"].queryset = restaurants
        self.fields["restaurant"].empty_label = "Choose a restaurant" if restaurants.exists() else "No restaurants yet - add one in Admin"



