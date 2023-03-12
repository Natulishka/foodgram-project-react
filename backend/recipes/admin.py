from django.contrib import admin

from recipes.models import Ingredient, MeasurementUnit, Tag

# class TitleAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'year', 'description')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'


# admin.site.register(Title, TitleAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MeasurementUnit)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Review)
