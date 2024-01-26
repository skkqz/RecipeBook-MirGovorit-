from django.db import models


class Product(models.Model):
    """
    Модель продукта.
    """
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    prepared_foods = models.IntegerField(default=0, verbose_name='Приготовленных блюд')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    products = models.ManyToManyField(Product, through='RecipeProduct')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    """
    Модель рецепта и входящих в него продуктов по граммам.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Название рецепта')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название продукта')
    weight = models.IntegerField(default=0, verbose_name='грамм')

    class Meta:
        verbose_name = 'Рецепт_продукт'
        verbose_name_plural = 'Рецепт_продукты'
        ordering = ['recipe']

    def __str__(self):
        return self.recipe.name
