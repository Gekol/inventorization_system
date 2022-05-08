import json
import time

from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types
from inventorization_service.models import Item
from rms_service.serializers import RepairSerializer


class TestInventoryService(APITestCase):

    def setUp(self) -> None:
        self.folder_name = "test_logs"
        self.file_name = "info.json"
        self.folder_name = f"/Users/georgesokolovsky/diploma/inventorization_system/tests/{self.folder_name}"
        # Initialise groups
        self.admin_group, self.repairman_group, self.specialist_group = initialise_test_groups(
            ["admin", "repairman", "specialist"])

        # Initialise users
        self.gekol, self.michael, self.oleksyi = initialise_test_users(
            [("gekol", ["admin"]), ("michael", ["repairman"]), ("oleksyi", ["specialist"])])

        # Initialise item types
        self.laptop_type = initialise_test_types(["Laptop"])[0]

        # Initialise items
        self.laptop1, self.laptop2, self.laptop3 = initialise_test_items(
            [("Laptop 1", 1, self.gekol, "broken"),
             ("Laptop 2", 1, self.michael, "broken"),
             ("Laptop 3", 1, self.oleksyi, "broken")])

        # Authenticate
        self.client.login(username="michael", password=MOCK_PASSWORD)

    def test_fix_item(self):
        data = {
            "fix_status": "ok"
        }
        response = self.client.put(f"/repair_service/{self.laptop_type.id}/items/{self.laptop1.id}/", data)
        self.assertEqual(response.data, RepairSerializer().to_representation(Item.objects.get(pk=self.laptop1.id)))

    def tearDown(self) -> None:
        time.sleep(1)
        with open(f"{self.folder_name}/{self.file_name}", "w") as f:
            f.write(json.dumps([]))
