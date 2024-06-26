from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )
    username = models.CharField('username', max_length=150, unique=True)
    email = models.EmailField('email', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user'
    )

    class Meta:
        ordering = ('role',)

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
