from django.urls import path

from advertisements import views

from .apps import AdvertisementsConfig

app_name = AdvertisementsConfig.name

urlpatterns = [
    # Advertisement
    path("advertisements/", views.AdvertisementListAPIView.as_view(), name="advertisement_list"),
    path(
        "advertisements/comments/",
        views.AdvertisementWithCommentsListAPIView.as_view(),
        name="advertisement_with_comments_list",
    ),
    path("advertisement/create/", views.AdvertisementCreateAPIView.as_view(), name="advertisement_create"),
    path(
        "advertisement/<int:pk>/",
        views.AdvertisementRetrieveAPIView.as_view(),
        name="advertisement_retrieve",
    ),
    path(
        "advertisement/<int:pk>/delete/",
        views.AdvertisementDeleteAPIView.as_view(),
        name="advertisement_delete",
    ),
    path(
        "advertisement/<int:pk>/update/",
        views.AdvertisementUpdateAPIView.as_view(),
        name="advertisement_update",
    ),
    # Comment
    path("comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comment/create/", views.CommentCreateAPIView.as_view(), name="comment_create"),
    path(
        "comment/<int:pk>/",
        views.CommentRetrieveAPIView.as_view(),
        name="comment_retrieve",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteAPIView.as_view(),
        name="comment_delete",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateAPIView.as_view(),
        name="comment_update",
    ),
    # Basket
    path(
        "advertisement/<int:pk>/add_ad_in_basket/",
        views.BasketItemCreateApiView.as_view(),
        name="add_ad_in_basket",
    ),
    path(
        "user/basket/",
        views.BasketListApiView.as_view(),
        name="user_basket",
    ),
]
