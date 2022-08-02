# from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# import datetime as dt
# from django.db.models import Avg

from reviews.models import Comment, Review
from reviews.models import Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Пользователь 'me' не корректен")
        return value

    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreTitleSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        try:
            genres_list = Genre.objects.get(slug=data)
        except Exception:
            raise serializers.ValidationError('Таких жанров нет!')
        print(genres_list)
        return genres_list

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        extra_kwargs = {'name': {'required': False}}


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы уже оставили отзыв!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
