from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework import routers

from api.views import UserViewSet, signup, token
from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

router_v1 = SimpleRouter()

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
