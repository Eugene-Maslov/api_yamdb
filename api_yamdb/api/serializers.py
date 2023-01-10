import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryField(SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreField(SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(queryset=Category.objects.all(),
                             slug_field='slug')
    genre = GenreField(queryset=Genre.objects.all(),
                       slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError('Неверный год выпуска!')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)
    email = serializers.EmailField(max_length=254,
                                   required=True)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User

    def validate(self, data):
        if User.objects.filter(email=data.get('email')).exists():
            user = User.objects.get(email=data.get('email'))
            if user.username != data.get('username'):
                raise ValidationError('invalid email')
        if User.objects.filter(username=data.get('username')).exists():
            user = User.objects.get(username=data.get('username'))
            if user.email != data.get('email'):
                raise ValidationError('invalid username')
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        if data.get('username').lower() == 'me':
            raise ValidationError('"me" is not valid username')
        if User.objects.filter(email=data.get('email')).exists():
            user = User.objects.get(email=data.get('email'))
            if user.username != data.get('username'):
                raise ValidationError('invalid email')
        if User.objects.filter(username=data.get('username')).exists():
            user = User.objects.get(username=data.get('username'))
            if user.email != data.get('email'):
                raise ValidationError('invalid username')
        return data

    class Meta:
        fields = ('username', 'email')
        model = User


class ConfirmRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
