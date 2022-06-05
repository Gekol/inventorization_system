from rest_framework.test import APITestCase
from core.asynchronous_messenger import AsynchronousMessenger


class TestAsynchronousMessengerStarter(APITestCase):
    def start_consumer(self):
        asynchronous_messenger = AsynchronousMessenger()
        asynchronous_messenger.run_consumer("test_logs",
                                            "/Users/georgesokolovsky/diploma/inventorization_system/tests/test_logs")


TestAsynchronousMessengerStarter().start_consumer()
