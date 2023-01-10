# Generated by Django 3.2 on 2023-01-10 15:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_remove_review_unique_author_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10, message='Введите значение от 1 до 10'), django.core.validators.MinValueValidator(1, message='Введите значение от 1 до 10')], verbose_name='Значение оценки'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_author_review'),
        ),
    ]
