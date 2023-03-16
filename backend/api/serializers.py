import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientRecipe, Recipe, Subscription,
                            Tag, TagRecipe)

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
        request = self.context.get('request')
        return Subscription.objects.filter(author=obj,
                                           subscriber=request.user
                                           ).exists()


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
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.name

    def get_name(self, obj):
        return obj.ingredient.name


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(many=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'name', 'is_in_shopping_cart', 'image', 'text',
        #           'cooking_time')
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')


class RecipesSubscriptionsSerializer(RecipesSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
        for ingredient in ingredients:
            ingredient = dict(ingredient)
            IngredientRecipe.objects.create(
                ingredient=ingredient['id'], recipe=recipe,
                amount=ingredient['amount'])
        return recipe

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
            for ingredient in ingredients_data:
                ingredient = dict(ingredient)
                IngredientRecipe.objects.create(
                    ingredient=ingredient['id'], recipe=instance,
                    amount=ingredient['amount'])
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance)
        return serializer.data


class SubscriptionSerializer(CustomUserSerializer):
    id = serializers.IntegerField(source='author_id')
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_id(self, obj):
        return obj.author.id

    def get_email(self, obj):
        return obj.author.email

    def get_username(self, obj):
        return obj.author.username

    def get_first_name(self, obj):
        return obj.author.first_name

    def get_last_name(self, obj):
        return obj.author.last_name

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get("recipes_limit")
        recipes = obj.author.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipesSubscriptionsSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


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
        serializer = SubscriptionSerializer(instance)
        return serializer.data
