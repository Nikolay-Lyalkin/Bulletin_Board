from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class MaterialsTestCase(APITestCase):

    def setUp(self):
        group = Group.objects.create(name="user")
        self.user = User.objects.create_user(
            username="test", email="test@yandex.ru", first_name="test", last_name="test", password="testpass"
        )
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        data = {
            "username": "test_create",
            "email": "test_create@yandex.ru",
            "first_name": "test_create",
            "last_name": "test_create",
            "password": "testpass",
        }

        response = self.client.post("/user/create/", data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(
            response.json(),
            {
                "username": "test_create",
                "email": "test_create@yandex.ru",
                "first_name": "test_create",
                "last_name": "test_create",
            },
        )

        self.assertTrue(User.objects.all().exists())

    def test_list_users(self):
        response = self.client.get(
            "/users/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            [{"username": "test", "email": "test@yandex.ru", "first_name": "test", "last_name": "test"}],
        )

    def test_patch_user(self):
        # Lesson.objects.create(name="Test_put", user=self.user)
        data = {"first_name": "TestPatch"}

        response = self.client.patch("/user/1/update/", data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {"username": "test", "email": "test@yandex.ru", "first_name": "TestPatch", "last_name": "test"},
        )

    def test_delete_user(self):
        response = self.client.delete("/user/1/delete/")

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_detail_user(self):
        response = self.client.get(
            "/user/1/",
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {"username": "test", "email": "test@yandex.ru", "first_name": "test", "last_name": "test"},
        )
