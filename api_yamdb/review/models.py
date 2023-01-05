from django.db import models
from django.contrib.auth.models import AbstractUser


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

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Categories, related_name='category',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genres, related_name='genre')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
