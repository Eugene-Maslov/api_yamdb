from django.urls import include, path

from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import registration, get_token, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', registration, name='registration'),
    path('auth/token/', get_token, name='token')
#    path('', include('djoser.urls')),
#    path('', include('djoser.urls.jwt')),
]
