from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from review.models import Categories, Genres, Titles, User
from .permissions import IsAdminOrReadOnly
from .serializers import CategoriesSerializer, GenresSerializer
from .serializers import TitlesSerializer
from .serializers import (UserSerializer, EditUserSerializer,
                          RegistrationSerializer, ConfirmRegistrationSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)


@api_view(["POST"])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="yamdb registration",
        message=f'Your secret code {confirmation_code}',
        from_email = None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_token(request):
    serializer = ConfirmRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    if default_token_generator.check_token(user,
                                           serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
