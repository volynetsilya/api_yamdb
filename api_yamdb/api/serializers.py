from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review, Category, Genre, Title
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


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254, required=True
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Пользователь "me" не корректен')
        elif User.objects.filter(username=value):
            raise serializers.ValidationError('Пользователь с таким именем '
                                              'уже зарегистрирован')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()):
            raise serializers.ValidationError(
                'Такая почта уже зарегистрирована'
            )
        return value


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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.HiddenField(
        default=serializers.SlugRelatedField(
            slug_field='name', read_only=True)
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
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
