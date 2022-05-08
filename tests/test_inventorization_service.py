import json
import time

from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types
from inventorization_service.models import Item
from inventorization_service.serializers import ItemSerializer, ItemUpdateSerializer


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
            [("Laptop 1", 1, self.gekol, "ok"), ("Laptop 2", 1, self.michael, "ok"),
             ("Laptop 3", 1, self.oleksyi, "ok")])

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
        self.assertEqual(response.data[0], ItemSerializer().to_representation(self.laptop1))
        self.assertEqual(response.data[1], ItemSerializer().to_representation(self.laptop2))
        self.assertEqual(response.data[2], ItemSerializer().to_representation(self.laptop3))

    def test_get_certain_item(self):
        response = self.client.get(f"/inventory_service/{self.laptop_type.id}/items/{self.laptop1.id}/")
        self.assertEqual(response.data, ItemSerializer().to_representation(self.laptop1))

    def test_create_new_item(self):
        data = {
            "name": "Laptop 4",
            "status": "in_use",
            "fix_status": "ok",
        }
        initial_objects_count = len(Item.objects.all())
        response = self.client.post(f"/inventory_service/{self.laptop_type.id}/items/", data=data)
        self.assertEqual(response.status_code, 201)
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
        with open(f"{self.folder_name}/{self.file_name}", "w") as f:
            f.write(json.dumps([]))
