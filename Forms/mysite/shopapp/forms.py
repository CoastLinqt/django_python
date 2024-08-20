from django import forms
from .models import Product, Order
from django.contrib.auth.models import Group


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount"
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
