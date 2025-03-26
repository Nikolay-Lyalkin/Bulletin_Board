from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from advertisements.permissions import IsAdmin, IsOwnerForModelUser, IsUser
from config.settings import PATH_RESET_PASSWORD
from users.models import User
from users.serializers import (UserCreateSerializer, UserResetPasswordConfirmSerializer, UserResetPasswordSerializer,
                               UserSerializer)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.is_active = True
        new_user.password = make_password(new_user.password)
        new_user.token = RefreshToken.for_user(new_user).access_token
        if new_user.role == "user":
            user_group = Group.objects.get(name="user")
            new_user.groups.add(user_group)
        elif new_user.role == "admin":
            user_group = Group.objects.get(name="admin")
            new_user.groups.add(user_group)
        new_user.save()


class UserResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = UserResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"<{PATH_RESET_PASSWORD}>/id пользователя - {uid}/токен пользователя - {user.token}"
            send_mail(
                "от Bulletin_Board",
                f"Пожалуйста, перейдите по следующей ссылке для сброса пароля: {reset_link}",
                "serega94nn@yandex.ru",
                [email],
            )
            return Response({"message": "Ссылка для сброса пароля выслана на ваш email."})
        return Response({"message": "Данный пользователь не найден."})


class UserResetPasswordConfirmAPIView(generics.CreateAPIView):
    serializer_class = UserResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):
        uid = urlsafe_base64_decode(request.data["id"]).decode("utf-8")
        token = request.data["token"]
        user = User.objects.filter(pk=uid, token=token).first()
        if user:
            user.password = make_password(request.data["password"])
            user.save()
            return Response("Пароль успешно изменён.")
        return Response("Данного пользователя не существует.")


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser | IsAdmin]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerForModelUser | IsAdmin]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerForModelUser | IsAdmin]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser | IsAdmin]
