from django.contrib import admin

from recipes.models import (ChoppingCart, Favorite, Ingredient,
                            IngredientRecipe, MeasurementUnit, Recipe,
                            Subscription, Tag)


class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    empty_value_display = '-пусто-'
    ordering = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    ordering = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'
    ordering = ('slug',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('measurement_unit',)
    list_display = ('pk', 'recipe', 'ingredient', 'measurement_unit', 'amount')
    empty_value_display = '-пусто-'
    ordering = ('recipe',)

    def measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.name


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('_ingredients', 'in_favorite')
    list_display = ('pk', 'name', 'pub_date', 'text', 'cooking_time', 'image',
                    'author', '_tags', '_ingredients')
    empty_value_display = '-пусто-'
    filter_horizontal = ('tags',)
    list_filter = ('name', 'author', 'tags')
    ordering = ('pub_date',)

    def _tags(self, obj):
        return ", ".join([t.slug for t in obj.tags.all()])

    def _ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj).values_list(
            'ingredient__name', 'ingredient__measurement_unit__name', 'amount')
        return ", ".join([f'{i[0]} ({i[1]}) - {i[2]}' for i in ingredients])

    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subscriber', 'author')
    empty_value_display = '-пусто-'
    ordering = ('author',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-пусто-'
    ordering = ('user',)


class ChoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-пусто-'
    ordering = ('user',)


admin.site.register(ChoppingCart, ChoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
