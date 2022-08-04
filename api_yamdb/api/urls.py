from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, get_token
from api.views import CategoriesViewSet, GenresViewSet, TitleViewSet
from api.views import CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet)

auth_patterns = [
    path('signup/', signup),
    path('token/', get_token),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
