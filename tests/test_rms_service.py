import json
import time
from datetime import datetime

from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types
from inventorization_service.models import Item
from rms_service.serializers import RepairSerializer


class TestInventoryService(APITestCase):

    def setUp(self) -> None:
        current_moment = datetime.now()
        self.folder_path = "tests/test_logs"
        self.severity = "info"
        self.file_name = f"{current_moment.year}_{current_moment.month}_{current_moment.day}.json"
        self.file_path = f"{self.folder_path}/{self.severity}/{self.file_name}"

        # Initialise groups
        self.admin_group, self.repairman_group, self.specialist_group = initialise_test_groups(
            ["admin", "repairman", "specialist"])

        # Initialise users
        self.gekol, self.michael, self.oleksyi = initialise_test_users(
            [("gekol", ["admin"]), ("michael", ["repairman"]), ("oleksyi", ["specialist"])])

        # Initialise item types
        self.laptop_type, self.cup_type = initialise_test_types([("Laptop", False), ("Cup", True)])

        # Initialise items
        self.laptop1, self.laptop2, self.laptop3 = initialise_test_items(
            [("Laptop 1", 1, self.gekol, "broken"), ("Laptop 2", 1, self.michael, "broken"),
             ("Laptop 3", 1, self.oleksyi, "broken")])

        # Authenticate
        self.client.login(username="gekol", password=MOCK_PASSWORD)

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
        with open(self.file_path, "w") as f:
            f.write(json.dumps([]))
