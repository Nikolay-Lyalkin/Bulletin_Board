from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from advertisements.models import Advertisement, Comment, BasketItem, Basket


class AdvertisementSerializer(ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ["title", "price", "description", "author", "created_at"]


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["text", "author", "ad", "created_at", "id"]


class AdvertisementCommentSerializer(ModelSerializer):
    advertisement_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ["title", "price", "description", "author", "created_at", "advertisement_comment"]


class AdvertisementRetrieveSerializer(ModelSerializer):
    advertisement_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ["title", "price", "description", "author", "created_at", "advertisement_comment"]


class BasketItemSerializer(ModelSerializer):

    class Meta:
        model = BasketItem
        fields = ["basket", "product"]


class BasketSerializer(ModelSerializer):

    class Meta:
        model = Basket
        fields = "__all__"

    def to_representation(self, instance):  # Кастомный вывод сериализатора
        representation = super().to_representation(instance)  # Получаем стандартное представление данных
        representation.pop('user', None)

        return representation


