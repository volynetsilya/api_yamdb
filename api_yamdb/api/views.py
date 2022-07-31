from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

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
    #permission_classes = (AdminOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (AdminOrReadOnly,)
