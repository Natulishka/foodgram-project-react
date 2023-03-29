import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import (ChoppingCart, Favorite, Ingredient,
                            IngredientRecipe, Recipe, Subscription, Tag,
                            TagRecipe)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени!')
        return data


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        if not self.context['subscribtions']:
            return False
        return obj.id in self.context.get('subscribtions', [])


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(source='ingredients_recipes',
                                             many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        if not self.context['favorites']:
            return False
        return obj.id in self.context.get('favorites', [])

    def get_is_in_shopping_cart(self, obj):
        if not self.context['shopping_carts']:
            return False
        return obj.id in self.context.get('shopping_carts', [])


class RecipesShortSerializer(RecipesSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        lst = []
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
            lst.append(tag)
        recipe.tags.set(lst)
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(ingredient=ingredient['id'], recipe=recipe,
                              amount=ingredient['amount'])
             for ingredient in ingredients])
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            TagRecipe.objects.filter(recipe_id=instance.id).delete()
            lst = []
            for tag in tags_data:
                TagRecipe.objects.create(tag=tag, recipe=instance)
                lst.append(tag)
            instance.tags.set(lst)
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            IngredientRecipe.objects.filter(recipe_id=instance.id).delete()
            IngredientRecipe.objects.bulk_create(
                [IngredientRecipe(ingredient=ingredient['id'], recipe=instance,
                                  amount=ingredient['amount'])
                 for ingredient in ingredients_data])
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance, context=self.context)
        return serializer.data


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.method == 'POST':
            recipes = obj.recipes.all()
        else:
            recipes_all = self.context.get('recipes', [])
            recipes = recipes_all.filter(author=obj)
        if request:
            recipes_limit = request.GET.get("recipes_limit")
            if recipes_limit:
                recipes = recipes[:int(recipes_limit)]
        serializer = RecipesShortSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ()
        model = Subscription

    def validate(self, data):
        request = self.context.get('request')
        author = get_object_or_404(
            User,
            pk=self.context.get('view').kwargs.get('id')
        )
        subscriber = request.user
        if request.method == 'POST':
            if author == subscriber:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!')
            if Subscription.objects.filter(author=author,
                                           subscriber=subscriber
                                           ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора!')
        return data

    def to_representation(self, instance):
        serializer = SubscriptionSerializer(instance.author,
                                            context=self.context)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ()
        model = Favorite

    def validate(self, data):
        request = self.context.get('request')
        recipe = get_object_or_404(
            Recipe,
            pk=self.context.get('view').kwargs.get('id')
        )
        user = request.user
        if (request.method == 'POST' and
            Favorite.objects.filter(recipe=recipe,
                                    user=user).exists()):
            raise serializers.ValidationError(
                'Этот рецепт уже есть в избранном!')
        return data

    def to_representation(self, instance):
        serializer = RecipesShortSerializer(instance.recipe)
        return serializer.data


class ChoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ()
        model = ChoppingCart

    def validate(self, data):
        request = self.context.get('request')
        recipe = get_object_or_404(
            Recipe,
            pk=self.context.get('view').kwargs.get('id')
        )
        user = request.user
        if (request.method == 'POST' and
            ChoppingCart.objects.filter(recipe=recipe,
                                        user=user).exists()):
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок!')
        return data

    def to_representation(self, instance):
        serializer = RecipesShortSerializer(instance.recipe)
        return serializer.data
