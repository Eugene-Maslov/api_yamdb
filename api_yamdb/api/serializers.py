import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from review.models import Category, Comment, Genre, Review, Title, User
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='name', many=True)
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='name')

    class Meta:
        model = Title
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
            UniqueValidator(queryset=User.objects.all())
        ]
)
    email = serializers.EmailField(validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    def validate_username(self, value):
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
