from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (ChoppingCartViewSet, FavoriteViewSet,
                       IngridientsViewSet, RecipesViewSet, SubscribeViewSet,
                       SubscriptionsViewSet, TagsViewSet)

app_name = 'api'

api_router = DefaultRouter()

api_router.register('ingredients', IngridientsViewSet)
api_router.register('tags', TagsViewSet)
api_router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('users/subscriptions/',
         SubscriptionsViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/subscribe/',
         SubscribeViewSet.as_view({
             'post': 'create',
             'delete': 'destroy'})),
    path('recipes/<int:id>/favorite/',
         FavoriteViewSet.as_view({
             'post': 'create',
             'delete': 'destroy'})),
    path('recipes/<int:id>/shopping_cart/',
         ChoppingCartViewSet.as_view({
             'post': 'create',
             'delete': 'destroy'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(api_router.urls)),
]
