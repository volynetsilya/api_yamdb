from rest_framework.exceptions import ValidationError

from users.models import User


def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            'Пользователь с таким именем уже существует!'
        )
    elif value == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            'Пользователь с таким email уже существует!'
        )
