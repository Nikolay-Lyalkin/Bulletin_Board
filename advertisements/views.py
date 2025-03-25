from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from advertisements.models import Advertisement, Comment
from advertisements.paginators import PaginationADS
from advertisements.permissions import IsUser, IsOwner, IsAdmin
from advertisements.serializers import (
    AdvertisementSerializer,
    CommentSerializer,
    AdvertisementCommentSerializer,
    AdvertisementRetrieveSerializer,
)


class AdvertisementListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    pagination_class = PaginationADS
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["created_at"]


class AdvertisementWithCommentsListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementCommentSerializer
    pagination_class = PaginationADS
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["created_at"]


class AdvertisementCreateAPIView(generics.CreateAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsUser | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdvertisementRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [IsUser | IsAdmin]


class AdvertisementDeleteAPIView(generics.DestroyAPIView):
    queryset = Advertisement.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwner | IsAdmin]


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    permission_classes = [IsUser | IsAdmin]


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsUser | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUser | IsAdmin]


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | IsAdmin]
