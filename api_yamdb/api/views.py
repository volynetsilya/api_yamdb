from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Titles

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer,
    TitlePostlesSerializer
)

#from .permissions import AdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer(partial=False)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genres__slug', 'year')
    #permission_classes = (AdminOrReadOnly,)

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
    #permission_classes = (AdminOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    #permission_classes = (AdminOrReadOnly,)
