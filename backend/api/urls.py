from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngridientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'api'

api_router = SimpleRouter()

api_router.register('ingredients', IngridientsViewSet)
api_router.register('tags', TagsViewSet)
api_router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(api_router.urls)),
]
