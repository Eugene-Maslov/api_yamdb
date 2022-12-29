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
