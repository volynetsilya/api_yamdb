from django.shortcuts import render
from rest_framework import viewsets

from reviews.models import Category, Genre, Titles

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer,
    TitlePostlesSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitlesSerializer
        return TitlePostlesSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
