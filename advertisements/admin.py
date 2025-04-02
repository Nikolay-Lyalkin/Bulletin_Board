from django.contrib import admin

from advertisements.models import Advertisement, Comment, Basket, BasketItem


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "ad")


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ("basket", "product")
