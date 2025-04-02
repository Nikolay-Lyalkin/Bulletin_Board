from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from advertisements.models import Advertisement, Comment, Basket, BasketItem
from advertisements.paginators import PaginationADS
from advertisements.permissions import IsAdmin, IsOwner, IsUser
from advertisements.serializers import (AdvertisementCommentSerializer, AdvertisementRetrieveSerializer,
                                        AdvertisementSerializer, CommentSerializer, BasketItemSerializer,
                                        BasketSerializer)


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


class BasketItemCreateApiView(generics.CreateAPIView):
    """ Добавляет товар в корзину """

    serializer_class = BasketItemSerializer

    def create(self, request, *args, **kwargs):
        basket = Basket.objects.filter(user=request.user).first()
        product = Advertisement.objects.filter(id=request.data["id"]).first()
        basket_item = BasketItem.objects.create(basket=basket, product=product)
        serializer = BasketItemSerializer(basket_item)
        message = "Товар добавлен в корзину"

        return Response({'message': message, 'data': serializer.data})


class BasketListApiView(generics.ListAPIView):
    """ Возвращает id товаров в корзине """

    serializer_class = BasketSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        basket = Basket.objects.filter(user=user).first()
        if basket:
            products_in_basket = BasketItem.objects.filter(basket=basket)
            serializer = self.get_serializer(products_in_basket, many=True)
            return Response({'data': serializer.data})
        else:
            return Response({'data': []})
