from rest_framework.serializers import ModelSerializer

from advertisements.serializers import BasketSerializer
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]


class UserResetPasswordSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]


class UserResetPasswordConfirmSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "token", "password"]
