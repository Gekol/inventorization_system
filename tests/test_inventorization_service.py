import json
import time
from datetime import datetime

from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types
from inventorization_service.models import Item
from inventorization_service.serializers import ItemSerializer, ItemUpdateSerializer


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
        self.laptop1, self.laptop2, self.laptop3, self.cup1, self.cup2, self.cup3 = initialise_test_items(
            [("Laptop 1", 1, self.gekol, "ok"), ("Laptop 2", 1, self.michael, "ok"),
             ("Laptop 3", 1, self.oleksyi, "ok"), ("Cup 1", 2, None, "ok"),
             ("Cup 2", 2, None, "ok"), ("Cup 3", 2, None, "ok")])

        # Authenticate
        self.client.login(username="gekol", password=MOCK_PASSWORD)

    def test_item_to_dict(self):
        self.assertEqual(self.laptop1.to_dict(), {
            'id': 1,
            "type": "Laptop",
            "name": "Laptop 1",
            "owner": "gekol",
            "status": "in_use",
            "fix_status": "ok",
            "broke_count": 0
        })

    def test_str(self):
        self.assertEqual(str(self.laptop1), "Id=1 Name='Laptop 1' Owner=gekol")

    def test_get_all_items(self):
        response = self.client.get(f"/inventory_service/{self.laptop_type.id}/items/")
        self.assertEqual(response.data[0], {
            "name": self.laptop1.name,
            "item_link": f'http://testserver/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/'
        })

    def test_get_certain_item(self):
        response = self.client.get(f"/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/")
        self.assertEqual(response.data, ItemSerializer().to_representation(self.laptop1))

    def test_create_new_item(self):
        data = {
            "name": "Laptop 4",
            "status": "in_warehouse",
            "fix_status": "ok",
        }
        initial_objects_count = len(Item.objects.all())
        response = self.client.post(f"/inventory_service/{self.laptop_type.id}/items/", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(initial_objects_count, len(Item.objects.all()) - 1)

    def test_update_item(self):
        data = {
            "owner": None,
            "status": "in_warehouse",
            "fix_status": "broken",
        }
        response = self.client.put(f"/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.get(pk=self.laptop1.id).broke_count, 1)
        self.laptop1 = Item.objects.get(pk=1)
        self.assertEqual(response.data, ItemUpdateSerializer().to_representation(self.laptop1))

    def test_permanent_extradition(self):
        data = {
            "status": "in_use",
            "fix_status": "ok",
        }
        initial_len = len(Item.objects.all())
        self.client.put(f"/inventory_service/{self.cup_type.id}/items/{self.cup1.id}/", data=data)
        self.assertEqual(initial_len, len(Item.objects.all()) + 1)

    def test_implicit_change_owner(self):
        data = {
            "owner": "",
            "status": "in_use",
            "fix_status": "ok",
        }
        response = self.client.put(f"/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.laptop1 = Item.objects.get(pk=1)
        self.assertEqual(response.data, ItemUpdateSerializer().to_representation(self.laptop1))

    def test_change_owner(self):
        data = {
            "owner": 2,
            "status": "in_use",
            "fix_status": "ok",
        }
        response = self.client.put(f"/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.laptop1 = Item.objects.get(pk=1)
        self.assertEqual(response.data, ItemUpdateSerializer().to_representation(self.laptop1))

    def tearDown(self) -> None:
        time.sleep(1)
        with open(f"{self.file_path}", "w") as f:
            f.write(json.dumps([]))
