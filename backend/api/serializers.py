import webcolors
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Tag

User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
