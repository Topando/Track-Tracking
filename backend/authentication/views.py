from drf_yasg import openapi
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class RegisterUserView(APIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя с отправкой email с кодом",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя',
                                           format=openapi.FORMAT_PASSWORD),
            },
        ),
        responses={
            201: openapi.Response('Created', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен пользователя'),
                    'uid': openapi.Schema(type=openapi.TYPE_STRING, description='Идентификатор пользователя'),
                }
            )),
            400: 'Неверные данные'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, uid = serializer.save()
        return Response({
            'token': token,
            'uid': uid,
        }, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    @swagger_auto_schema(
        operation_description="Подтверждение почты",
        manual_parameters=[
            openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Токен пользователя'),
            openapi.Parameter('uid', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Идентификатор пользователя'),
            openapi.Parameter('code', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Код подтверждения'),
        ],
        responses={
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Пользователь'),
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен пользователя'),
                }
            )),
            400: 'Неверные данные'
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user is not None:
            return Response({
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1],
            })
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Авторизация пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя (необязательно)'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя (необязательно)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя',
                                           format=openapi.FORMAT_PASSWORD),
            },
        ),
        responses={
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Пользователь'),
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен пользователя'),
                }
            )),
            400: 'Неверные данные'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })
