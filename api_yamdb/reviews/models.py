import datetime as dt
from django.db import models
from django.core.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError("Год выпуска не может быть больше текущего!")
    return value


class Category(models.Model):
    """
    Model representing a Title category (e.g. "Books", "Movies", "Music" ...).
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Model representing a Title genre (e.g. "science fiction", "novel" ...).
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """
    A model representing a creative work that belongs to a category.
    """
    name = models.TextField()
    year = models.IntegerField(validators=(validate_year, ))
    description = models.TextField()
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitles'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            ),
        ]

    def __str__(self):
        return self.name


# В этой модели связаны id жанра и id произведения Titles
class GenreTitles(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            ),
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'
