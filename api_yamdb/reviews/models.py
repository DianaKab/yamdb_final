import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Класс экземпляра пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        blank=False, null=False,
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        blank=False, null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True, null=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True, null=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True, null=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
        blank=False, null=False,
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4(),
        editable=False,
        unique=False,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = (
            models.UniqueConstraint(
                fields=('username', 'confirmation_code',),
                name='unique_username_confirmation_code'
            ),
        )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField('Год публикации')
    description = models.TextField(null=True)
    rating = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)
    score = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    class Meta:
        ordering = ['pub_date']

        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]
