from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (ChoppingCartViewSet, FavoriteViewSet,
                       IngridientsViewSet, RecipesViewSet, SubscribeViewSet,
                       SubscriptionsViewSet, TagsViewSet,
                       download_shopping_cart_view)

app_name = 'api'

api_router = SimpleRouter()

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
    path('recipes/download_shopping_cart/',
         download_shopping_cart_view),
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
