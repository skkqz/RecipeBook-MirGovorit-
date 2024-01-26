from django.urls import path
from .views import AddProductToRecipeView, CookRecipeView, ShowRecipesWithoutProductView, GetReceptView

urlpatterns = [
    path('add_product_to_recipe/', AddProductToRecipeView.as_view(), name='add_product_to_recipe'),
    path('cook_recipe/', CookRecipeView.as_view(), name='cook_recipe'),
    path('show_recipes_without_product/<int:pk>', ShowRecipesWithoutProductView.as_view(),
         name='show_recipes_without_product'),
    path('get/<int:pk>', GetReceptView.as_view(), name='get_recipes'),
]
