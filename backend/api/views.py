from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.exceptions import BadRequestException
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (ChoppingCartSerializer, FavoriteSerializer,
                             IngredientsSerializer, RecipesPostSerializer,
                             RecipesSerializer, SubscribeSerializer,
                             SubscriptionSerializer, TagsSerializer)
from api.utils import make_file
from api.viewsets import CreateDestroyViewSet, ListViewSet
from recipes.models import (ChoppingCart, Favorite, Ingredient,
                            IngredientRecipe, Recipe, Subscription, Tag)

User = get_user_model()


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = IngredientFilter
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

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = '_' + request.user.username
        content_type = {'.txt': 'text/plain',
                        '.pdf': 'application/pdf'}
        recipes = Recipe.objects.filter(recipe_sh__user=request.user)
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=recipes).values(
                'ingredient__name',
                'ingredient__measurement_unit__name').annotate(
                    amount=Sum('amount')).order_by('ingredient__name',
                                                   'amount')
        file = settings.PREF + settings.FILENAME + user
        make_file(file, settings.EXT, ingredients)
        return FileResponse(open(file + settings.EXT, 'rb'),
                            as_attachment=True,
                            content_type=content_type[settings.EXT])


class SubscriptionsViewSet(ListViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            id__in=user.subscriber.values('author_id'))


class SubscribeViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_object(self):
        author = get_object_or_404(User, pk=self.kwargs['id'])
        subscriber = self.request.user
        if not Subscription.objects.filter(author=author,
                                           subscriber=subscriber).exists():
            raise BadRequestException(
                {'errors': 'Вы не подписаны на этого автора!'})
        return get_object_or_404(Subscription, subscriber=subscriber,
                                 author=author)

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs['id'])
        serializer.save(subscriber=self.request.user, author=author)


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('recipe',)

    def get_object(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['id'])
        user = self.request.user
        if not Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
            raise BadRequestException(
                {'errors': 'Этого рецепта нет в избранном!'},)
        return get_object_or_404(Favorite, user=user,
                                 recipe=recipe)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)


class ChoppingCartViewSet(CreateDestroyViewSet):
    queryset = ChoppingCart.objects.all()
    serializer_class = ChoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('recipe',)

    def get_object(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['id'])
        user = self.request.user
        if not ChoppingCart.objects.filter(user=user,
                                           recipe=recipe).exists():
            raise BadRequestException(
                {'errors': 'Этого рецепта нет в списке покупок!'})
        return get_object_or_404(ChoppingCart, user=user,
                                 recipe=recipe)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)
