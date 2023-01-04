from django.db import models


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
