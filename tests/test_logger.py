import json
import time

from rest_framework.test import APITestCase

from core.logger import Logger


class TestLogger(APITestCase):
    def setUp(self) -> None:
        self.folder_path = "test_logs"
        self.file_path = f"/Users/georgesokolovsky/PycharmProjects/" \
                         f"inventorization_system/tests/{self.folder_path}/info.json"
        self.logger = Logger()

    def test_emit_log(self):
        severity = "info"
        message = {
            "item_id": 6,
            "item_name": "Lenovo ThinkPad T15g Gen 1",
            "username": "gekol",
            "message": "Item fixed"
        }
        self.logger.emit_log(severity, json.dumps(message))
        time.sleep(5)
        logs = json.loads(open(self.file_path, "r").read())[0]["data"]
        self.assertEqual(logs, message)

    def tearDown(self) -> None:
        with open(self.file_path, "w") as f:
            f.write(json.dumps([]))
