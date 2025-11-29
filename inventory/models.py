from django.db import models

# Create your models here.
class Ingredients(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    units =models.CharField(max_length=5)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f" Item: {self.title} - Price: {self.price}"

class RecipieRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.units} of {self.ingredient.name} for {self.menu_item.title}"

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchased {self.menu_item.title}x{self.quantity} on {self.time_stamp}"
