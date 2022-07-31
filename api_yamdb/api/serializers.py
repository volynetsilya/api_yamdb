from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

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
        exclude = ('id')


class SingUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=254, validators=[validate_email]
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[validate_username]
    )
    token = serializers.CharField(max_length=50)

    class Meta:
        model = User
        firlds = ('username', 'code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        token = default_token_generator.make_token(user)
        if str(token) != data['code']:
            raise ValidationError('Неверный код подтверждения!')
        return data