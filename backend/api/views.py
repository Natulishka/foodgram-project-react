from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (IngredientsSerializer, RecipesPostSerializer,
                             RecipesSerializer, SubscribeSerializer,
                             SubscriptionSerializer, TagsSerializer)
from api.viewsets import CreateDestroyViewSet, ListViewSet
from recipes.models import Ingredient, Recipe, Subscription, Tag

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
    ordering = ('-pub_date',)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipesPostSerializer
        return RecipesSerializer


class SubscriptionsViewSet(ListViewSet):
    # queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


class SubscribeViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

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
