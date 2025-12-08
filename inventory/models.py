from django.db import models

# Create your models here.
class Ingredients(models.Model):
    UNIT_CHOICES = [
        ("Kg", "Kilogram (kg)"),
        ("G", "Gram (g)"),
        ("L", "Liter (l)"),
        ("Ml", "Milliliter (ml)"),
        ("Oz", "Ounces (oz)"),
        ("Pcs", "Pieces"),
    ]
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    units =models.CharField(max_length=5, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.units})"

class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f" Item: {self.title} - Price: {self.price}"

class RecipieRequirements(models.Model):
    UNIT_CHOICES = [
        ("Kg", "Kilogram (kg)"),
        ("G", "Gram (g)"),
        ("L", "Liter (l)"),
        ("Ml", "Milliliter (ml)"),
        ("Oz", "Ounces (oz)"),
        ("Pcs", "Pieces"),
    ]
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    required_units = models.CharField(max_length=5, choices=UNIT_CHOICES, default="Pcs")
    class Meta:
        unique_together = ('menu_item', 'ingredient')
        
    def __str__(self):
        return f"{self.quantity} {self.required_units} of {self.ingredient.name} for {self.menu_item.title}"

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchased {self.menu_item.title}x{self.quantity} on {self.time_stamp}"
