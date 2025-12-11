from django.urls import path
from .views import ( 
    InventoryView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    MenuItemDeleteView,
    MenuListView,
    MenuItemCreateView,
    MenuItemUpdateView,
    RecipieRequirementsCreateView,
    PurchaseCreateView,
    PurchaseListView,
    FinanceReportView,
    HomeView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('inventory/list/', InventoryView.as_view(), name='inventory-list'),
    path('inventory/list/add/', IngredientCreateView.as_view(), name='ingredient-add'),
    path('ingredient/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient-update'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/add/', MenuItemCreateView.as_view(), name='menu-item-add'),
    path("menu/update/<int:pk>/", MenuItemUpdateView.as_view(), name="update-menu-item"),
    path("menu/delete/<int:pk>/", MenuItemDeleteView.as_view(), name="delete-menu-item"),
    path('recipie-requirements/add/', RecipieRequirementsCreateView.as_view(), name='recipie-requirements-add'),
    path('purchases/add/', PurchaseCreateView.as_view(), name='purchase-add'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('finance-report/', FinanceReportView.as_view(), name='finance-report'),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
