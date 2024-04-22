from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .utils import *

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def save(self, **kwargs):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.is_active = False
        user.save()

        send_confirmation_email(user, self.context['request'])
        return user

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            if user:
                if not user.check_password(password):
                    user = None
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
