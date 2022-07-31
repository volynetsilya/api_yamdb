from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = None
    email = models.CharField(max_length=254)
    bio = models.TextField('Биография', blank=True,)
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Адмитнистратор'),
        (MODERATOR, 'Модератор'),
    )
    role = models.TextField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return self.username


    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR