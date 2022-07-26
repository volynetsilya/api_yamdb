from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = None
    email = models.CharField(max_length=254)
    bio = models.TextField('Биография', blank=True,)
    USER = 1
    MODERATOR = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.TextField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return self.username
