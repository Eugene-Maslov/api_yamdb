from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    roles = [(USER, 'user'),
             (MODER, 'moderator'),
             (ADMIN, 'admin')]

    username = models.CharField(max_length=150,
                                verbose_name='Username',
                                unique=True)

    email = models.EmailField(verbose_name='Email adress',
                              unique=True)

    bio = models.CharField(null=True,
                           blank=True,
                           verbose_name='about_me',
                           max_length=500)

    role = models.CharField(choices=roles,
                            default='user',
                            max_length=50)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Значение оценки',
        validators=[
            MaxValueValidator(10, message='Введите значение от 1 до 10'),
            MinValueValidator(1, message='Введите значение от 1 до 10')
        ]
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=300
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
