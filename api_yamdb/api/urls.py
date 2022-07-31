from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, token
from .views import CategoriesViewSet, GenresViewSet, TitleViewSet
from .views import CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()

router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
