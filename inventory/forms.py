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

MenuItemFormSet = forms.inlineformset_factory(
    MenuItem,
    RecipieRequirements,
    fields=('ingredient', 'quantity', 'required_units'),
    extra=5,
    can_delete= False
)

class RecipieRequirementsForm(forms.ModelForm):
    class Meta:
        model = RecipieRequirements
        fields = ['ingredient', 'quantity', 'required_units']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['menu_item', 'quantity']