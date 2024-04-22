from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, uid = serializer.save()
        return Response({
            'token': token,
            'uid': uid,
        }, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        uid = kwargs.get('uid')
        code = kwargs.get('code')

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

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })
