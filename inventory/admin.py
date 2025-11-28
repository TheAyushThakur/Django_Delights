from django.contrib import admin
from .models import Ingredients, MenuItem, RecipieRequirements, Purchase

admin.site.register(Ingredients)
admin.site.register(MenuItem)
admin.site.register(RecipieRequirements)
admin.site.register(Purchase)
