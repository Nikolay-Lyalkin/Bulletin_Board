from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from advertisements.models import Advertisement, Comment
from users.models import User


class AdvertisementTestCase(APITestCase):

    def setUp(self):
        group = Group.objects.create(name="admin")
        self.user = User.objects.create_user(
            username="test", email="test@yandex.ru", first_name="test", last_name="test", password="testpass"
        )
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)
        self.ad = Advertisement.objects.create(title="test", author=self.user)
        self.comment = Comment.objects.create(text="testcomment", author=self.user, ad=self.ad)

    def test_create_ad(self):
        data = {
            "title": "test_create",
        }

        response = self.client.post("/advertisement/create/", data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Advertisement.objects.all().exists())

    def test_list_ad(self):

        response = self.client.get(
            "/advertisements/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_patch_ad(self):

        data = {"title": "TestPatch"}

        response = self.client.patch("/advertisement/1/update/", data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json().get("title"),
            "TestPatch",
        )

    def test_delete_ad(self):
        response = self.client.delete("/advertisement/1/delete/")

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_detail_ad(self):
        response = self.client.get(
            "/advertisement/1/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        data = {"text": "test_comment_create", "ad": 1, "author": 1}

        response = self.client.post("/comment/create/", data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Comment.objects.all().exists())

    def test_list_comment(self):

        response = self.client.get("/comments/")

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json()[0].get("text"), "testcomment")

    def test_patch_comment(self):

        data = {"text": "TestCommentPatch"}

        response = self.client.patch("/comment/1/update/", data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json().get("text"),
            "TestCommentPatch",
        )

    def test_delete_comment(self):
        response = self.client.delete("/comment/1/delete/")

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Comment.objects.all().exists())

    def test_detail_comment(self):
        response = self.client.get(
            "/comment/1/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json().get("text"), "testcomment")

    def test_list_ad_with_comment(self):

        response = self.client.get(
            "/advertisements/comments/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json().get("results")[0].get("advertisement_comment")[0].get("text"), "testcomment")
