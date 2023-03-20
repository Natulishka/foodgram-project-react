import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters

from recipes.models import Favorite, Ingredient, Recipe, Tag

CHOICES = ((1, 1), (0, 0))


def favorite(request):
    if request is None:
        return Favorite.objects.none()
    user = request.user
    return Favorite.objects.filter(user=user)


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.ChoiceFilter(choices=CHOICES,
                                        method='filter_is_favorited')
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=CHOICES,
        method='filter_is_in_shopping_cart')
    author = filters.NumberFilter(field_name='author_id')
    tags = filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                             field_name='tags__slug',
                                             to_field_name='slug')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == '0':
            return Recipe.objects.exclude(recipe__user=user).all()
        return Recipe.objects.filter(recipe__user=user).all()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == '0':
            return Recipe.objects.exclude(recipe_sh__user=user).all()
        return Recipe.objects.filter(recipe_sh__user=user).all()


class IngredientFilter(django_filters.FilterSet):

    name = filters.CharFilter(method='filter_name')

    def filter_name(self, queryset, name, value):
        return Ingredient.objects.filter(Q(name__istartswith=value) |
                                         Q(name__icontains=value))
