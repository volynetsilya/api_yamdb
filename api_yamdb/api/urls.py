from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)

urlpatterns = [
    #path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
