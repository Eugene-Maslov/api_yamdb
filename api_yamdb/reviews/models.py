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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(db_index=True)
    category = models.ForeignKey(Category, related_name='category',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, related_name='genre')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('category',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=300
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Значение оценки',
        validators=[
            MaxValueValidator(10, message='Введите значение от 1 до 10'),
            MinValueValidator(1, message='Введите значение от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"

    def __str__(self):
        return self.text[:15]
