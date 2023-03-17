import os

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (ChoppingCartSerializer, FavoriteSerializer,
                             IngredientsSerializer, RecipesPostSerializer,
                             RecipesSerializer, SubscribeSerializer,
                             SubscriptionSerializer, TagsSerializer)
from api.viewsets import CreateDestroyViewSet, ListViewSet
from recipes.models import (ChoppingCart, Favorite, Ingredient,
                            IngredientRecipe, Recipe, Subscription, Tag)

FILENAME = 'chopping_cart.txt'
User = get_user_model()


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    search_fields = ('^name',)
    ordering = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    ordering = ('name',)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    ordering = ('-pub_date',)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipesPostSerializer
        return RecipesSerializer


class SubscriptionsViewSet(ListViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


class SubscribeViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_object(self):
        return get_object_or_404(Subscription, subscriber=self.request.user,
                                 author=self.kwargs['id'])

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs['id'])
        serializer.save(subscriber=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(
            User,
            pk=self.kwargs['id']
        )
        subscriber = request.user
        if not Subscription.objects.filter(
                  author=author,
                  subscriber=subscriber).exists():
            return Response(['Вы не подписаны на этого автора!'],
                            status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('recipe',)

    def get_object(self):
        return get_object_or_404(Favorite, user=self.request.user,
                                 recipe=self.kwargs['id'])

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs['id']
        )
        user = request.user
        if not Favorite.objects.filter(
                  user=user,
                  recipe=recipe).exists():
            return Response(['Этого рецепта нет в избранном!'],
                            status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChoppingCartViewSet(CreateDestroyViewSet):
    queryset = ChoppingCart.objects.all()
    serializer_class = ChoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('recipe',)

    def get_object(self):
        return get_object_or_404(ChoppingCart, user=self.request.user,
                                 recipe=self.kwargs['id'])

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs['id']
        )
        user = request.user
        if not ChoppingCart.objects.filter(user=user,
                                           recipe=recipe).exists():
            return Response(['Этого рецепта нет в списке покупок!'],
                            status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def download_shopping_cart_view(request):
    recipes = Recipe.objects.filter(recipe_ch__user=request.user)
    ingredients = IngredientRecipe.objects.filter(
        recipe__in=recipes).values(
        'ingredient__name',
        'ingredient__measurement_unit__name'
        ).annotate(amount=Sum('amount')).order_by('ingredient__name', 'amount')
    with open(FILENAME, 'w', encoding='utf-8') as f:
        f.write('Choping cart:' + '\n')
        f.write('\n')
        counter = 1
        for ingredient in ingredients:
            line = (f"{counter}. {ingredient['ingredient__name'].capitalize()}"
                    f" ({ingredient['ingredient__measurement_unit__name']}) - "
                    f"{ingredient['amount']} \n")
            f.write(line)
            counter += 1
        f.write('\n')
        f.write('\n')
        f.write('Created by Foodgtam' + '\n')
        f.write('Author: Shulgina Natalya')
    return FileResponse(open(FILENAME, 'rb'), as_attachment=True)
