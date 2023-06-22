from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class RegisterTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint = "/api/auth/register/"
        return super().setUp()

    def test_register_without_first_and_last_name(self):
        request_data = {
            "username": "test_user",
            "email": "test_user@test.test",
            "password": "password",
        }

        response = self.client.post(self.endpoint, request_data)
        assert response.status_code == 200

        users = get_user_model().objects.all()

        assert len(users) == 1

        created_user = get_user_model().objects.get(username="test_user")

        assert created_user.username == "test_user"
        assert created_user.email == "test_user@test.test"
        assert not created_user.first_name
        assert not created_user.last_name

    def test_register_with_names(self):
        request_data = {
            "username": "test_user",
            "email": "test_user@test.test",
            "password": "password",
            "first_name": "First",
            "last_name": "Last",
        }

        response = self.client.post(self.endpoint, request_data)
        assert response.status_code == 200

        users = get_user_model().objects.all()

        assert len(users) == 1

        created_user = get_user_model().objects.get(username="test_user")

        assert created_user.username == "test_user"
        assert created_user.email == "test_user@test.test"
        assert created_user.first_name == "First"
        assert created_user.last_name == "Last"

    def test_error_register_with_first_name(self):
        request_data = {
            "username": "test_user",
            "email": "test_user@test.test",
            "password": "password",
            "first_name": "First",
        }

        response = self.client.post(self.endpoint, request_data)

        assert response.status_code == 400
        assert response.json() == ["First and last names are required!"]

        users = get_user_model().objects.all()

        assert len(users) == 0

    def test_error_register_with_last_name(self):
        request_data = {
            "username": "test_user",
            "email": "test_user@test.test",
            "password": "password",
            "last_name": "Last",
        }

        response = self.client.post(self.endpoint, request_data)

        assert response.status_code == 400
        assert response.json() == ["First and last names are required!"]

        users = get_user_model().objects.all()

        assert len(users) == 0


class LoginTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint = "/api/auth/login/"
        self.user = get_user_model()(
            username="test_user",
            email="test_user@test.test",
            first_name="First",
            last_name="Last",
        )
        self.user.set_password("password")
        self.user.save()
        return super().setUp()

    def test_login_user(self):
        request_data = {
            "email": "test_user@test.test",
            "password": "password",
        }

        response = self.client.post(self.endpoint, request_data)

        assert response.status_code == 200
        assert response.json().get("email", False)
        assert response.json().get("username", False)
        assert response.json().get("first_name", False)
        assert response.json().get("last_name", False)
        assert response.json().get("tokens", False)
        assert response.json()["tokens"].get("access", False)
        assert response.json()["tokens"].get("refresh", False)

    def test_error_login_invalid_password(self):
        request_data = {
            "email": "test_user@test.test",
            "password": "invalid_password",
        }

        response = self.client.post(self.endpoint, request_data)

        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect email or password!"}
