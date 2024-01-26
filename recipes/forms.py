from django import forms
from .models import RecipeProduct, Product, Recipe


class AddProductToRecipeForm(forms.ModelForm):
    """
    Форма для добавления - изменения продуктов в рецепте.
    """

    class Meta:
        model = RecipeProduct
        fields = ['recipe', 'product', 'weight', ]


class CookRecipeForm(forms.ModelForm):
    """
    Форма для увеличивает на единицу количество приготовленных блюд для каждого продукта.
    """

    class Meta:
        model = Recipe
        fields = ['name', 'products']
