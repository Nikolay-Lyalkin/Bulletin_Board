from rest_framework.serializers import ModelSerializer

from advertisements.models import Advertisement, Comment


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
