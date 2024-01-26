from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.db import transaction
from .models import Recipe, Product, RecipeProduct
from .forms import AddProductToRecipeForm, CookRecipeForm


class GetReceptView(generic.DetailView):
    """
    Представление для отображения рецепта и продуктов в нём.
    """

    model = Recipe
    template_name = 'recipes/get_recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_in_recipe'] = RecipeProduct.objects.filter(recipe=self.kwargs['pk'])
        return context


class AddProductToRecipeView(generic.FormView):
    """
    Представление для добавления или обновления продуктов рецепте.
    """

    model = Recipe
    template_name = 'recipes/add_product_to_recipe.html'
    form_class = AddProductToRecipeForm
    success_url = reverse_lazy('add_product_to_recipe')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()
        context['products'] = Product.objects.all()
        return context

    def form_valid(self, form):
        form.save(commit=False)
        recipe = form.cleaned_data['recipe']
        product = form.cleaned_data['product']
        weight = form.cleaned_data['weight']

        recipe_product = RecipeProduct.objects.get_or_create(recipe=recipe, product=product)[0]
        if recipe_product:
            recipe_product.weight = weight
            recipe_product.save()

        return super().form_valid(form)


class CookRecipeView(generic.TemplateView):
    """
    Представление для увеличивает на единицу количество приготовленных блюд для каждого продукта.
    """

    form_class = CookRecipeForm
    template_name = 'recipes/cook_recipe.html'
    success_url = reverse_lazy('cook_recipe')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)

        with transaction.atomic():
            for recipe_product in recipe.recipeproduct_set.all():
                recipe_product.product.prepared_foods += 1
                recipe_product.product.save()

        return redirect('cook_recipe')


class ShowRecipesWithoutProductView(generic.TemplateView):
    """
     Представление возвращает HTML страницу, на которой размещена таблица.
     В таблице отображены id и названия всех рецептов, в которых указанный
     продукт отсутствует, или присутствует в количестве меньше 10 грамм.
    """

    template_name = 'recipes/show_recipes_without_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        context['recipes_without_product'] = Recipe.objects.exclude(recipeproduct__product=self.kwargs['pk']).distinct()
        recipes_with_low_quantity = RecipeProduct.objects.filter(
            product=self.kwargs['pk'], weight__lt=10).values_list('recipe', flat=True)
        context['recipes_with_low_quantity'] = Recipe.objects.filter(pk__in=recipes_with_low_quantity)
        return context
