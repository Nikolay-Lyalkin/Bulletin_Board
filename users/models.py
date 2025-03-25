from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(unique=True, max_length=30, verbose_name="Никнейм пользователя")
    email = models.EmailField(unique=True, max_length=50, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=30, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия пользователя")
    phone_number = models.CharField(verbose_name="Номер телефона", blank=True, null=True, max_length=20)
    image = models.FileField(upload_to="avatars/", verbose_name="Ваша фотография", blank=True, null=True)
    token = models.CharField(max_length=1000, verbose_name="Токен", blank=True, null=True)
    role = models.CharField(verbose_name="Роль", blank=True, null=True, default="user", max_length=5)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "users"

    def __str__(self):
        return f"{self.email}"
