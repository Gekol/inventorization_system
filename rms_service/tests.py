from rest_framework.test import APITestCase

from core.create_functions import initialise_test_groups, initialise_test_users, MOCK_PASSWORD, \
    initialise_test_items
from inventorization_service.models import Item
from rms_service.serializers import RepairSerializer


class TestInventoryService(APITestCase):

    def setUp(self) -> None:
        # Initialise groups
        self.admin_group, self.repairman_group, self.specialist_group = initialise_test_groups(
            ["admin", "repairman", "specialist"])

        # Initialise users
        self.gekol, self.michael, self.oleksyi = initialise_test_users(
            [("gekol", ["admin"]), ("michael", ["repairman"]), ("oleksyi", ["specialist"])])

        # Initialise items
        self.laptop1, self.laptop2, self.laptop3 = initialise_test_items(
            [("Laptop 1", self.gekol, "broken"),
             ("Laptop 2", self.michael, "broken"),
             ("Laptop 3", self.oleksyi, "broken")])

        # Authenticate
        self.client.login(username="michael", password=MOCK_PASSWORD)

    def test_fix_item(self):
        data = {
            "fix_status": "ok"
        }
        response = self.client.put(f"/repair_system/{self.laptop1.id}/", data)
        self.assertEqual(response.data, RepairSerializer().to_representation(Item.objects.get(pk=self.laptop1.id)))
        print()
