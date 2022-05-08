from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types


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

    def test_item_type_to_dict(self):
        self.assertEqual(self.laptop_type.to_dict(), {
            "id": 1,
            "name": "Laptop",
            "min_amount": 3,
            "is_permanent": False
        })

    def test_item_type_to_str(self):
        self.assertEqual(str(self.laptop_type), "Laptop")
