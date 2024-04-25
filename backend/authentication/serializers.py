from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from userprofile.models import ConfirmEmailUser

from .utils import *

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30, min_length=5)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def validate_username(self, value):
        value = serializers.CharField().to_internal_value(value)
        user = User.objects.filter(username=value).first()
        if user is not None and not user.is_active:
            user.delete()
        return value

    def validate_email(self, value):
        value = serializers.EmailField().to_internal_value(value)
        user = User.objects.filter(email=value).first()
        if user is not None and not user.is_active:
            user.delete()
        return value

    def save(self, **kwargs):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.is_active = False
        user.save()

        code = create_token_check_email(user)
        if send_confirmation_email(user, code):
            return encode_user(user)
        else:
            return None

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


class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
    code = serializers.IntegerField()

    def save(self, **kwargs):
        token = self.validated_data.get('token')
        uid = self.validated_data.get('uid')
        code = self.validated_data.get('code')
        user = get_user_by_token_email(token, uid)
        if user is not None:
            confirm = ConfirmEmailUser.objects.filter(user=user, code=code).first()
            if confirm:
                confirm.delete()
                return user
        return None
