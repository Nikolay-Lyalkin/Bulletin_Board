from django.db import models

from users.models import User


class Advertisement(models.Model):
    title = models.CharField(verbose_name="Название товара", max_length=250)
    price = models.PositiveIntegerField(verbose_name="Цена", blank=True, null=True)
    description = models.TextField(verbose_name="Описание товара", blank=True, null=True, max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_advertisement",
        verbose_name="пользователь",
    )
    created_at = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        db_table = "advertisements"


class Comment(models.Model):
    text = models.TextField(verbose_name="Содержание отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_ad_comment",
        verbose_name="пользователь",
    )
    ad = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="advertisement_comment",
        verbose_name="Отзыв о товаре",
    )
    created_at = models.DateField(verbose_name="Дата публикации", auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = "comments"


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_basket",
        verbose_name="пользователь",
    )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        db_table = "basket"


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="basket_item",
        verbose_name="корзина с товарами",
    )
    product = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="ad_in_basket",
        verbose_name="товар в корзине",
    )

    def __str__(self):
        return f"{self.basket} - {self.product}"

    class Meta:
        verbose_name = "Корзина c товаром"
        verbose_name_plural = "Корзины с товаром"
        db_table = "basket_item"
