from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from auth_service.serializers import UserSerializer
from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD


class TestAuthService(APITestCase):

    def setUp(self) -> None:
        self.folder_name = "test_logs"
        self.file_name = "info.json"
        self.folder_name = f"/Users/georgesokolovsky/diploma/inventorization_system/tests/{self.folder_name}"
        # Initialise groups
        self.admin_group, self.repairman_group, self.specialist_group = initialise_test_groups(
            ["admin", "repairman", "specialist"])

        # Initialise users
        self.gekol, self.michael, self.oleksyi = initialise_test_users(
            [("gekol", ["admin"]), ("michael", ["repairman"]), ("oleksyi", ["specialist"])]
        )

        # Authenticate
        self.client.login(username="gekol", password=MOCK_PASSWORD)

    def test_get_all_users(self):
        response = self.client.get("/users/")
        self.assertEqual(response.data[0], UserSerializer().to_representation(self.gekol))
        self.assertEqual(response.data[1], UserSerializer().to_representation(self.michael))
        self.assertEqual(response.data[2], UserSerializer().to_representation(self.oleksyi))

    def test_get_certain_user(self):
        response = self.client.get(f"/users/{self.oleksyi.id}/")
        self.assertEqual(response.data, UserSerializer().to_representation(self.oleksyi))

    def test_add_new_user(self):
        data = {
            "first_name": "Olga",
            "last_name": "Sokolovska",
            "username": "olga_sokolovska",
            "password": MOCK_PASSWORD,
            "email": "sokolovskaya@gmail.com",
            "groups": [3]
        }
        initial_objects_count = len(User.objects.all())
        response = self.client.post("/users/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(User.objects.all()), initial_objects_count + 1)

    def test_update_user(self):
        data = {
            "groups": [3]
        }
        response = self.client.put(f"/users/{self.oleksyi.id}/", data)
        groups = [group.id for group in User.objects.get(id=self.oleksyi.id).groups.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(groups, [3])

    def test_delete(self):
        initial_objects_count = len(User.objects.all())
        self.client.delete(f"/users/{self.oleksyi.id}/")
        self.assertEqual(len(User.objects.all()), initial_objects_count - 1)
