import json
import time
from datetime import datetime

from rest_framework.test import APITestCase

from core.analytics import get_lacking_item_types, get_relation, get_lacking_types_messages
from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items, initialise_test_types


class TestAnalyticsService(APITestCase):
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

    def test_get_all_item_types(self):
        response = self.client.get("/inventory_service/")
        self.assertEqual(response.data, [
            {
                "item_type": self.laptop_type.name,
                "item_type_info": f'http://testserver/inventory_service/{self.laptop_type.id}/',
                'items': f'http://testserver/inventory_service/{self.laptop_type.id}/items/'
            },
            {
                "item_type": self.cup_type.name,
                "item_type_info": f'http://testserver/inventory_service/{self.cup_type.id}/',
                'items': f'http://testserver/inventory_service/{self.cup_type.id}/items/'
            }
        ])

    def test_get_lacking_item_types(self):
        expected = [self.laptop_type.to_dict(), self.cup_type.to_dict()]
        result = get_lacking_item_types()
        self.assertEqual(result, expected)

    def test_relation(self):
        expected = dict(self.laptop_type.to_dict(),
                        **{"in_use": 3,
                           "total": 3,
                           "relation": 100})
        result = get_relation()
        self.assertEqual(dict(result[0].to_dict(),
                              **{"in_use": result[0].in_use,
                                 "total": result[0].total,
                                 "relation": result[0].relation}), expected)

    def test_get_lacking_types_messages(self):
        expected = [f"We are missing items of type Laptop. The relation of its current usage is equal to 100.0%. "
                    f"We should buy 1 items of that type.",
                    f"The number of the items of type Laptop is less than the minimum equal to 3.",
                    f"The number of the items of type Cup is less than the minimum equal to 3."
                    ]
        result = get_lacking_types_messages()
        self.assertEqual(result, expected)

    def test_item_type_to_str(self):
        self.assertEqual(str(self.laptop_type), "Laptop")

    def test_item_type_to_dict(self):
        self.assertEqual(self.laptop_type.to_dict(), {
            "id": 1,
            "name": "Laptop",
            "min_amount": 3,
            "is_permanent": False
        })

    def test_get_analytics(self):
        expected = [dict(self.laptop_type.to_dict(),
                         **{"in_use": 3,
                            "total": 3,
                            "relation": 100})]
        response = self.client.get("/analytics_service/")
        self.assertEqual(expected, response.data)

    def tearDown(self) -> None:
        time.sleep(1)
        with open(f"{self.file_path}", "w") as f:
            f.write(json.dumps([]))
