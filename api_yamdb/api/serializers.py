from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt
from django.db.models import Avg

from reviews.models import Comment, Review
from reviews.models import Category, Genre, GenreTitle, Title
from api.validators import validate_username, validate_email
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=254, validators=[validate_email]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=254, validators=[validate_email]
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[validate_username]
    )
    confirmation_code = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения!')
        return data


# class GengeTpe(serializers.Field):
#     def to_representation(self, value):
#         print(value)
#         return value

#     def to_internal_value(self, data):
#         genres_list = Genre.objects.filter(slug__in=data)
#         if genres_list.count() != len(data):
#             raise serializers.ValidationError({'genres': 'Таких жанров нет!'})
#         return genres_list


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        extra_kwargs = {'name': {'required': False}}


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
    # rating = serializers.IntegerField()
    #    Title.objects.annotate(rating=Avg('reviews__score'))
    # )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(value):
        year = dt.date.today().year
        if value > year:
            raise ValidationError("Год выпуска не может быть больше текущего!")
        return value


class TitlePostlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genres = GenreTitleSerializer(
        many=True,
    #    rating = serializers.IntegerField()
    )
    #        Title.objects.annotate(
    #             rating=Avg('reviews__score'))
    #     )
    # )

    def create(self, validated_data):
        genres_to_write = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)
        print(title)
        for genre in genres_to_write:
            GenreTitle.objects.create(title=title, genre=genre)
        return (title)

    class Meta:
        fields = '__all__'
        model = Title
        extra_kwargs = {
            'description': {'required': False},
            'category': {'required': True},
            'rating': {'required': False},
        }


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

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title_id']
            )
        ]

        # def validate


class CommentSerializer(serializers.ModelSerializer):
    # review = serializers.SlugRelatedField(
    #     slug_field='text',
    #     read_only=True
    # )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
