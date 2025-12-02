from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView
from django.db.models import Sum, F
from .models import Ingredients, MenuItem, RecipieRequirements, Purchase
from .forms import IngredientForm, MenuItemForm, RecipieRequirementsForm, PurchaseForm, MenuItemFormSet
from django.shortcuts import redirect, render
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'inventory/home.html'
class InventoryView(ListView):
    model = Ingredients
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'ingredients'

class IngredientCreateView(CreateView):
    model = Ingredients
    form_class = IngredientForm
    template_name = 'forms/add_ingredient.html'
    success_url = '/inventory/list/'

    
class IngredientUpdateView(UpdateView):
    model = Ingredients
    form_class = IngredientForm
    template_name = 'forms/update_ingredient.html'
    success_url = '/inventory/list/'

    
class IngredientDeleteView(DeleteView):
    model = Ingredients
    template_name = 'inventory/ingredient_delete.html'
    success_url = '/inventory/list/'

class MenuListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu_list.html'
    context_object_name = 'menu_items'

class MenuItemCreateView(CreateView):
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

class RecipieRequirementsCreateView(CreateView):
    model = RecipieRequirements
    form_class = RecipieRequirementsForm
    template_name = 'forms/add_recipie_requirement.html'
    success_url = '/menu/'

class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "forms/add_purchase.html"
    success_url = '/purchases/'

    def form_valid(self, form):
        purchase = form.save(commit=False)
        item = purchase.menu_item
        quantity = purchase.quantity  

        requirements = RecipieRequirements.objects.filter(menu_item=item)

        for req in requirements:
            needed = req.quantity * quantity
            available = req.ingredient.quantity

            if needed > available:
                messages.error(
                    self.request,
                    f"Not enough {req.ingredient.name} to make {quantity}x {item.title}!"
                )
                return redirect("add-purchase")

        for req in requirements:
            req.ingredient.quantity -= req.quantity * quantity
            req.ingredient.save()

        return super().form_valid(form)


class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class FinanceReportView(TemplateView):
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
    
