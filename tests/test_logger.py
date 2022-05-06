import json
import time
from collections import namedtuple

from rest_framework.test import APITestCase

from core.logger import Logger, get_callback


class TestLogger(APITestCase):
    def setUp(self) -> None:
        self.folder_path = "test_logs"
        self.file_name = "info.json"
        self.folder_path = f"/Users/georgesokolovsky/PycharmProjects/inventorization_system/tests/{self.folder_path}"
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
        logs = json.loads(open(f"{self.folder_path}/{self.file_name}", "r").read())[0]["data"]
        self.assertEqual(logs, message)

    def test_get_callback(self):
        callback_function = get_callback(self.folder_path)
        Method = namedtuple("Method", "routing_key")
        method = Method("info")
        message = {
            "item_id": 6,
            "item_name": "Lenovo ThinkPad T15g Gen 1",
            "username": "gekol",
            "message": "Item fixed"
        }
        callback_function("", method, "", json.dumps(message))
        logs = json.loads(open(f"{self.folder_path}/{self.file_name}", "r").read())[0]["data"]
        self.assertEqual(logs, message)

    def tearDown(self) -> None:
        with open(f"{self.folder_path}/{self.file_name}", "w") as f:
            f.write(json.dumps([]))
