from django.db import transaction

from rest_framework.test import APITestCase

from movie_service.models import User

from . import init_users_and_groups


class SignalsTests(APITestCase):
    data = {
        'user': {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'TestUserP@ssword!',
        },
    }

    @classmethod
    def setUpTestData(cls):
        init_users_and_groups(cls)

    def test_on_create_user_init_settings(self):
        user = User.objects.create_user(**self.data['user'])
        self.assertEqual(user.groups.all().first().pk, self.group_user.pk)

    def test_on_create_user_assign_group(self):
        with transaction.atomic():
            user = User.objects.create_user(**self.data['user'])
            self.assertEqual(
                user.groups.all().first().pk, self.group_user.pk,
                msg='New user should have User group assigned'
            )
            transaction.set_rollback(True)

        admin = User.objects.create_superuser(**self.data['user'])
        self.assertEqual(
            admin.groups.all().first().pk, self.group_admin.pk,
            msg='New superuser should have Administrator group assigned'
        )
