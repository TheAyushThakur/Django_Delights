from django import forms
from .models import Ingredients, MenuItem, RecipieRequirements, Purchase

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name', 'quantity', 'units', 'price_per_unit']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']

class RecipieRequirementsForm(forms.ModelForm):
    class Meta:
        model = RecipieRequirements
        fields = ['menu_item', 'ingredient', 'quantity']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['menu_item', 'quantity']