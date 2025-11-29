from django.contrib import admin
from .models import MenuItem, Ingredients, RecipieRequirements, Purchase

class RecipeRequirementInline(admin.TabularInline):
    model = RecipieRequirements
    extra = 0  # number of blank ingredient fields to show

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [RecipeRequirementInline]

admin.site.register(Ingredients)
admin.site.register(Purchase)
