from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """
    Model representing a Title category (e.g. "Books", "Movies", "Music" ...).
    """
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    """
    Model representing a Title genre (e.g. "science fiction", "novel" ...).
    """
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    """
    A model representing a creative work that belongs to a category.
    """
    name = models.CharField(max_length=256, unique=True)
    year = models.IntegerField(db_index=True)
    description = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle' # связь???
    )
    category = models.ForeignKey(
        Category,
        related_name='title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    rating = models.IntegerField(
        null=True,
        default=None
    )

    class Meta:
        ordering = ('category', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            ),
        ]


# В этой модели связаны id жанра и id произведения Title
class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            ),
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        # contraints
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
