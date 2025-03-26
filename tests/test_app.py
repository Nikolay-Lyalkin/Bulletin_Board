import pytest
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APIClient

from advertisements.models import Advertisement, Comment
from users.models import User


@pytest.fixture
def user(db):
    group = Group.objects.create(name="admin")
    user = User.objects.create_user(
        username="test",
        email="test@yandex.ru",
        first_name="test",
        last_name="test",
        password="testpass",
    )
    user.groups.add(group)

    return user


@pytest.mark.django_db
def test_ad(user):
    client = APIClient()

    response = client.post("/user/token/", {"email": user.email, "password": "testpass"})
    access_token = response.json().get("access")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    data_ad_create = {
        "title": "test_create",
    }
    data_ad_patch = {"title": "TestPatch"}

    response_create = client.post("/advertisement/create/", data=data_ad_create)
    response_get = client.get("/advertisements/")
    response_get_comment = client.get("/advertisements/comments/")
    response_patch = client.patch("/advertisement/1/update/", data=data_ad_patch)
    response_detail = client.get("/advertisement/1/")

    assert response_create.status_code == status.HTTP_201_CREATED
    assert Advertisement.objects.all().exists()

    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json().get("results")[0].get("title") == "test_create"
    assert response_get_comment.status_code == status.HTTP_200_OK

    assert response_patch.status_code == status.HTTP_200_OK
    assert response_patch.json().get("title") == "TestPatch"

    assert response_detail.status_code == status.HTTP_200_OK

    response_delete = client.delete("/advertisement/1/delete/")

    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    assert not Advertisement.objects.all().exists()


@pytest.mark.django_db
def test_comment(user):
    client = APIClient()

    response = client.post("/user/token/", {"email": user.email, "password": "testpass"})
    access_token = response.json().get("access")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    data_comment_create = {"text": "test_create", "ad": 2}
    data_comment_patch = {"text": "TestPatch"}
    data_ad_create = {"title": "test_create"}

    client.post("/advertisement/create/", data=data_ad_create)
    response_comment_create = client.post("/comment/create/", data=data_comment_create)
    response_get = client.get("/comments/")
    response_patch = client.patch("/comment/1/update/", data=data_comment_patch)
    response_detail = client.get("/comment/1/")

    assert response_comment_create.status_code == status.HTTP_201_CREATED
    assert Comment.objects.all().exists()

    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json()[0].get("text") == "test_create"

    assert response_patch.status_code == status.HTTP_200_OK
    assert response_patch.json().get("text") == "TestPatch"

    assert response_detail.status_code == status.HTTP_200_OK

    response_delete = client.delete("/comment/1/delete/")

    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.all().exists()


@pytest.mark.django_db
def test_user(user):
    client = APIClient()

    Group.objects.create(name="user")

    data_user_create = {
        "username": "test_create",
        "email": "test_create@yandex.ru",
        "first_name": "test_create",
        "last_name": "test_create",
        "password": "testpass",
        "role": "admin",
    }
    data_user_patch = {"username": "TestPatch"}

    response_user_create = client.post("/user/create/", data=data_user_create)

    response = client.post("/user/token/", {"email": "test@yandex.ru", "password": "testpass"})
    access_token = response.json().get("access")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response_get = client.get("/users/")
    response_patch = client.patch("/user/3/update/", data=data_user_patch)
    response_detail = client.get("/user/3/")

    assert response_user_create.status_code == status.HTTP_201_CREATED
    assert User.objects.all().exists()

    assert response.status_code == status.HTTP_200_OK

    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json() == [
        {"email": "test@yandex.ru", "first_name": "test", "last_name": "test", "username": "test"},
        {
            "email": "test_create@yandex.ru",
            "first_name": "test_create",
            "last_name": "test_create",
            "username": "test_create",
        },
    ]

    assert response_patch.status_code == status.HTTP_200_OK
    assert response_patch.json().get("username") == "TestPatch"

    assert response_detail.status_code == status.HTTP_200_OK

    response_delete = client.delete("/user/3/delete/")

    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
