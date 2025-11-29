from django.urls import path
from .views import InventoryView, IngredientDeleteView, MenuListView, PurchaseListView, FinanceReportView, HomeView

urlpatterns = [
    path('inventory/list/', InventoryView.as_view(), name='inventory-list'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('finance-report/', FinanceReportView.as_view(), name='finance-report'),
    path("", HomeView.as_view(), name="home"),
]
