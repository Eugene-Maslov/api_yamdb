from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from review.models import Categories, Genres, Titles, User

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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        UniqueValidator(queryset=User.objects.all())],
        required=True,)
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class EditUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_field = ('role',)
        model = User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())])

    def validate_username(self,value):
        if value.lower() == 'me':
            raise ValidationError('"me" is not valid username')
        return value
    
    class Meta:
        fields = ('username', 'email')
        model = User


class ConfirmRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
