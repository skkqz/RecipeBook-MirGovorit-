from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Product, RecipeProduct


class RecipeTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product')
        self.recipe = Recipe.objects.create(name='Test Recipe')
        self.recipe_product = RecipeProduct.objects.create(
            recipe=self.recipe, product=self.product, weight=100
        )

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('get_recipes', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')
        self.assertContains(response, 'Test Product')

    def test_add_product_to_recipe_view(self):
        response = self.client.post(reverse('add_product_to_recipe'), {
            'recipe': self.recipe.id,
            'product': self.product.id,
            'weight': 200
        })
        self.assertEqual(response.status_code, 302)  # 302 - перенаправление после успешного сохранения
        self.assertEqual(RecipeProduct.objects.filter(recipe=self.recipe, product=self.product).count(), 1)
        self.assertEqual(RecipeProduct.objects.get(recipe=self.recipe, product=self.product).weight, 200)

    def test_cook_recipe_view(self):
        response = self.client.post(reverse('cook_recipe'), {'recipe_id': self.recipe.id})
        self.assertEqual(response.status_code, 302)  # 302 - перенаправление после успешного сохранения
        self.assertEqual(Product.objects.get(id=self.product.id).prepared_foods, 1)

    def test_show_recipes_without_product_view(self):
        response = self.client.get(reverse('show_recipes_without_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
