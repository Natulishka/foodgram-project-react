from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

app_name = 'api'

api_router = SimpleRouter()

# api_router.register(
#     'users',
#     UserViewSet,
#     basename='users'
# )

urlpatterns = [
    # path('auth/token/login/', SignupViewSet.as_view({'post': 'create'})),
    # path('auth/token/logout/', TokenViewSet.as_view({'post': 'create'}),
    #      name='token_obtain_pair'),
    # path('', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]