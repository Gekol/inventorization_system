import json
import os
from django.test import TestCase

import inventorization_system.settings as settings

import django
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from auth_service.views import UserViewSet

django.setup()


class TestAuthServiceWithAdmin(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='gekol', password="1111")
        self.user = User.objects.get(username='gekol')
        self.factory = APIRequestFactory()
        request = self.factory.get('/api-auth/login/?next=/users/')
        force_authenticate(request, user=self.user)
        self.view = UserViewSet.as_view({'get': 'list'})

    def test_get_all_users(self):
        request = self.factory.get('/accounts/django-superstars/')
        request.user = self.user
        response = self.view(request)
        # print(json.loads())
        print(response.data)
