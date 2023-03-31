from django.contrib import admin
from django.utils.safestring import mark_safe

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


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('in_favorite', '_image')
    list_display = ('pk', 'name', 'pub_date', 'text', 'cooking_time', '_image',
                    'author', '_tags', '_ingredients')
    empty_value_display = '-пусто-'
    filter_horizontal = ('tags',)
    list_filter = ('name', 'author', 'tags')
    ordering = ('-pub_date',)
    inlines = [IngredientRecipeInline]

    def _image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" '
                         f'style="max-height: 100px;">')

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


admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ChoppingCart, ChoppingCartAdmin)
