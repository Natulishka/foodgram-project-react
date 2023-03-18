from django.contrib import admin

from recipes.models import Ingredient, MeasurementUnit, Recipe, Tag

# class TitleAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'year', 'description')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date', 'text', 'cooking_time', 'image',
                    'author') # 'get_tags', 
    empty_value_display = '-пусто-'
    filter_horizontal = ('tags',)

    # def get_tags(self, obj):
    #     return "\n".join([t.name for t in obj.tags.all()])


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasurementUnit)
admin.site.register(Tag, TagAdmin)
