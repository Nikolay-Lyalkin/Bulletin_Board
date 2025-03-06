from rest_framework import generics
from rest_framework.filters import OrderingFilter

from advertisements.models import Advertisement, Comment
from advertisements.serializers import AdvertisementSerializer, CommentSerializer, AdvertisementCommentSerializer


class AdvertisementListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]


class AdvertisementWithCommentsListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementCommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

class AdvertisementCreateAPIView(generics.CreateAPIView):
    serializer_class = AdvertisementSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdvertisementRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class AdvertisementDeleteAPIView(generics.DestroyAPIView):
    queryset = Advertisement.objects.all()


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
