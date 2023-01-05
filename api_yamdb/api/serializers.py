from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import Categories, Genres, Titles

import datetime as dt


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(queryset=Genres.objects.all(),
                             slug_field='name', many=True)
    category = SlugRelatedField(queryset=Categories.objects.all(),
                                slug_field='name')

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        #fields = '__all__'

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError('Неверный год выпуска!')
        return value
