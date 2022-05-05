from rest_framework.test import APITestCase
from core.logger import Logger


class TestLogServerStarter(APITestCase):
    def start_server(self):
        logger = Logger()
        logger.run_server("/Users/georgesokolovsky/PycharmProjects/inventorization_system/tests/test_logs")


TestLogServerStarter().start_server()
