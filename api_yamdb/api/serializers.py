from django.urls import is_valid_path
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, GenreTitles, Titles


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        extra_kwargs = {'name': {'required': False}}


class TitlesSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=True)
    category = SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlePostlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genres = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    def create(self, validated_data):
        if self.is_valid():
            genres = validated_data.pop('genres')
            if len(set(genres)) < len(genres):
                raise serializers.ValidationError('Одинаковых жанров не должно быть!')
            title = Titles.objects.create(**validated_data)
            for genre in genres:
                GenreTitles.objects.create(
                genre=genre, title=title)
            return title

    class Meta:
        fields = '__all__'
        model = Titles
        extra_kwargs = {'description': {'required': False}, 'category': {'required': True}}
