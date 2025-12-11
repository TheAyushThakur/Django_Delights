from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView
from django.db.models import Sum, F
from django.views import View
from .models import Ingredients, MenuItem, RecipieRequirements, Purchase
from .forms import IngredientForm, MenuItemForm, RecipieRequirementsForm, PurchaseForm, MenuItemFormSet
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal


UNIT_CONVERSION = {
    "KG": Decimal("1000"),
    "G": Decimal("1"),

    "L": Decimal("1000"),
    "ML": Decimal("1"),
    
    "OZ": Decimal("28.3495"),

    "PCS": Decimal("1"),
}
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'
class InventoryView(LoginRequiredMixin, ListView):
    model = Ingredients
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'ingredients'

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredients
    form_class = IngredientForm
    template_name = 'forms/add_ingredient.html'
    success_url = '/inventory/list/'

    
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredients
    form_class = IngredientForm
    template_name = 'forms/update_ingredient.html'
    success_url = '/inventory/list/'

    
class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredients
    template_name = 'inventory/ingredient_delete.html'
    success_url = '/inventory/list/'

class MenuListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'inventory/menu_list.html'
    context_object_name = 'menu_items'

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'forms/add_menu_item.html'
    def get(self, request):
        item_form = MenuItemForm()
        formset = MenuItemFormSet()
        return render(request, self.template_name, {
            "item_form": item_form,
            "formset": formset
        })

    def post(self, request):
        item_form = MenuItemForm(request.POST)
        formset = MenuItemFormSet(request.POST)

        if item_form.is_valid() and formset.is_valid():
            menu_item = item_form.save()
            formset.instance = menu_item
            formset.save()
            return redirect("menu-list")

        return render(request, self.template_name, {
            "item_form": item_form,
            "formset": formset
        })

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "forms/menu_item_update.html"
    success_url = "/menu/"

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'inventory/menu_item_delete.html'
    success_url = '/menu/'
class RecipieRequirementsCreateView(LoginRequiredMixin, CreateView):
    model = RecipieRequirements
    form_class = RecipieRequirementsForm
    template_name = 'forms/add_recipie_requirement.html'
    success_url = '/menu/'

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "forms/add_purchase.html"
    success_url = '/purchases/'

    def form_valid(self, form):

        purchase = form.save(commit=False)
        item = purchase.menu_item
        order_qty = purchase.quantity  

        requirements = RecipieRequirements.objects.filter(menu_item=item)

        for req in requirements:
            ingredient = req.ingredient

            # convert recipe requirement to base unit
            required_amount = req.quantity * UNIT_CONVERSION[req.required_units.upper()]

            available_amount = ingredient.quantity * UNIT_CONVERSION[ingredient.units.upper()]

            total_needed = required_amount * order_qty

            if total_needed > available_amount:
                messages.error(
                    self.request,
                    f"Not enough {ingredient.name} available!"
                )
                return redirect("purchase-add")

        # Now deduct stock safely
        for req in requirements:
            ingredient = req.ingredient

            deduct_amount = (req.quantity * UNIT_CONVERSION[req.required_units.upper()]) * order_qty
            ingredient.quantity -= deduct_amount / UNIT_CONVERSION[ingredient.units.upper()]
            ingredient.save()

        return super().form_valid(form)

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class FinanceReportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/finance_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_revenue = Purchase.objects.aggregate(
            revenue = Sum(F('menu_item__price') * F('quantity')) 
        )['revenue'] or 0


        total_cost = 0
        purchases = Purchase.objects.all()
        for purchase in purchases:
            reqs = RecipieRequirements.objects.filter(menu_item=purchase.menu_item)

            for req in reqs:
                ingredient_cost = req.ingredient.price_per_unit* req.quantity
                total_cost += ingredient_cost* purchase.quantity

        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = total_revenue - total_cost
        return context
    
class LoginView(LoginView):
    template_name = 'auth/login.html'

class LogoutView(LogoutView):
    pass