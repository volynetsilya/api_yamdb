from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from reviews.models import Review, Title, Category, Genre, Title
from api.serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, ReadOnlyTitleSerializer,
    UserSerializer, SignUpSerializer, TokenSerializer,
    CommentSerializer, ReviewSerializer
)
from api.permissions import (
    IsAuthor, AdminOrReadOnly,
    AdminOnly, IsAdminModeratorOwnerOrReadOnly
)
from api.filters import TitlesFilter
from api_yamdb.settings import EMAIL_FOR_AUTH_LETTERS


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthor, IsAuthenticated)
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.role != 'user':
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    email = serializer.data['email']
    if (User.objects.filter(username=username)
            or User.objects.filter(email=email)):
        raise ValidationError(
            'Пользователь с таким именем или почтой уже зарегистрирован')
    user, _ = User.objects.get_or_create(username=username,
                                         email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения', confirmation_code, EMAIL_FOR_AUTH_LETTERS,
        [serializer.data['email']], fail_silently=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(
        {'confimation_code': 'Код подтверждения неверный'},
        status=status.HTTP_400_BAD_REQUEST
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg(
        'reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
