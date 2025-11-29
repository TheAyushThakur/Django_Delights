from django.views.generic import TemplateView
from django.db.models import Sum, F
from .models import Ingredients, MenuItem, RecipieRequirements, Purchase

class ReportView(TemplateView):
    template_name = "inventory/report.html"

    def get_context_data(self, **kwargs):
        
        context =   super().get_context_data(**kwargs)

        context["inventory"] = Ingredients.objects.all()

        context["purchases"] = Purchase.objects.all()

        context["menu_items"] = MenuItem.objects.all()

        total_revenue = Purchase.objects.aggregate(
            revenue = Sum(F('menu_item__price')*F('quantity'))
        ) ['revenue'] or 0
        context["total_revenue"] = total_revenue

        total_cost = 0
        for purchase in Purchase.objects.all():
            reqs = RecipieRequirements.objects.filter(menu_item=purchase.menu_item)

            for req in reqs:
                ingredient_cost = req.ingredient.price_per_unit * req.quantity
                total_cost += ingredient_cost * purchase.quantity

        context['total_cost'] = total_cost

        context['profit'] = total_revenue - total_cost

        return context
        
