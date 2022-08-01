from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
# router.register(r'reviews', ReviewViewSet)
# router.register(r'comments', CommentViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
