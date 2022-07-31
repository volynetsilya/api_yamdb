from django.shortcuts import render, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, viewsets
from rest_framework import viewsets

from users.models import User
from reviews.models import Review, Title
from reviews.models import Category, Genre, Titles
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer,
    TitlePostlesSerializer
)
from api.serializers import UserSerializer, SignUpSerializer, TokenSerializer
from api.serializers import CommentSerializer, ReviewSerializer
from api.permissions import AdminOnly, AccountOwnerOnly, IsAdminModeratorOwnerOrReadOnly
from api_yamdb.settings import EMAIL_FOR_AUTH_LETTERS


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(AccountOwnerOnly, IsAuthenticated)
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
    if not User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
        serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения', confirmation_code, EMAIL_FOR_AUTH_LETTERS,
        [request.data['email']], fail_silently=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer(partial=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genres__slug', 'year')
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSerializer
        return TitlePostlesSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
