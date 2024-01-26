from django.contrib import admin
from .models import RecipeProduct, Recipe, Product


@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):

    list_display = ['recipe', 'product', 'weight', ]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'prepared_foods', ]
