from django.db import transaction
from django.urls import reverse

from rest_framework import status

from movie_service.models import User

from . import AbstractApiModelAuthTests


class ApiUserAuthTests(AbstractApiModelAuthTests):
    SELF_UPDATE_FIELDS = ['photo', 'settings', 'watchlist']
    NOT_SELF_UPDATE_FIELDS = ['email', 'username', 'password']
    OPTIONALLY_HIDDEN_FIELDS = {
        'achievements': {
            'always_hidden': {
                'detail': False,
                'list': True
            }
        },
        'watchlist': {
            'always_hidden': {
                'detail': False,
                'list': True
            }
        },
        'email': {
            'always_hidden': {
                'detail': False,
                'list': False
            }
        }
    }
    HIDDEN_FIELDS = {
        'settings': {
            'always_hidden': {
                'detail': False,
                'list': True
            }
        },
    }
    rev_urls = {
        'list': 'user-list',
        'detail': 'user-detail',
    }
    data = {
        'user_01': {
            'username': 'testuser01',
            'email': 'testuser01@example.com',
            'password': 'TestUser01P@ss!'
        },
        'user_02': {
            'username': 'testuser02',
            'email': 'testuser02@example.com',
            'password': 'TestUser02P@ss!',
            'photo': None,
            'watchlist': [],
            'settings': {
                'email_visible': False,
                'watchlist_visible': False,
                'achievements_visible': False,
            },
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.admin, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'delete': [
                (cls.root, status.HTTP_204_NO_CONTENT),
                (cls.admin, status.HTTP_204_NO_CONTENT),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'update': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'partial_update': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'list': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_200_OK),
                (None, status.HTTP_200_OK),
            ],
            'retrieve': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_200_OK),
                (None, status.HTTP_200_OK),
            ],
        }

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse(self.rev_urls['list']), self.data['user_01'], format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_create_access(self):
        self.helper_test_general_access(
            self.actions_tests['create'],
            self.helper_test_create_access
        )

    def helper_test_delete_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_user = User.objects.create_user(**self.data['user_01'])
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_user.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_delete_access(self):
        self.helper_test_general_access(
            self.actions_tests['delete'],
            self.helper_test_delete_access
        )

    def helper_test_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_user = User.objects.create_user(**self.data['user_01'])
        modified_user = self.data['user_01'].copy()
        modified_user['email'] = self.data['user_02']['email']
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_user.pk}),
            data=modified_user, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['update'],
            self.helper_test_update_access
        )

    def helper_test_partial_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_user = User.objects.create_user(**self.data['user_01'])
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_user.pk}),
            data={'email': self.data['user_02']['email']}, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_partial_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['partial_update'],
            self.helper_test_partial_update_access
        )

    def helper_test_list_access(self, user, expected_status):
        self.client.force_authenticate(user)
        response = self.client.get(reverse(self.rev_urls['list']), format='json')
        self.assertEqual(response.status_code, expected_status)

    def test_list_access(self):
        self.helper_test_general_access(
            self.actions_tests['list'],
            self.helper_test_list_access
        )

    def helper_test_retrieve_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_user = User.objects.create_user(**self.data['user_01'])
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_user.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )

    def helper_test_self_partial_update_field(
            self, field, expected_status=status.HTTP_200_OK, client=None,
            msg=None):
        user = User.objects.create_user(**self.data['user_01'])
        if client is None:
            client = user

        self.client.force_authenticate(client)
        modified_part_user = {
            field: self.data['user_02'][field]
        }
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': user.pk}),
            data=modified_part_user, format='json'
        )
        self.assertEqual(response.status_code, expected_status, msg=msg)

    def test_self_partial_update_access(self):
        for field in self.SELF_UPDATE_FIELDS:
            with self.subTest(
                    field=field, expected_status=status.HTTP_200_OK),\
                    transaction.atomic():
                self.helper_test_self_partial_update_field(field, status.HTTP_200_OK)
                transaction.set_rollback(True)

    def test_self_partial_update_access_fail(self):
        for field in self.NOT_SELF_UPDATE_FIELDS:
            with self.subTest(
                    field=field, expected_status=status.HTTP_403_FORBIDDEN), \
                    transaction.atomic():
                self.helper_test_self_partial_update_field(
                    field, status.HTTP_403_FORBIDDEN,
                    msg=f'Field {field} should not be self updatable'
                )
                transaction.set_rollback(True)

        for field in self.SELF_UPDATE_FIELDS:
            with self.subTest(
                    field=field, expected_status=status.HTTP_403_FORBIDDEN),\
                    transaction.atomic():
                self.helper_test_self_partial_update_field(
                    field, status.HTTP_403_FORBIDDEN,
                    client=self.user,
                    msg=f'Field {field} should not be updatable without proper'
                        f' permissions. It\'s only allowed in self update case'
                )
                transaction.set_rollback(True)

    def helper_test_hidden_field(
            self, field, fields_dict, client, user, is_visible=False, msg=None):
        self.client.force_authenticate(client)
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': user.pk}),
            format='json'
        )
        if is_visible and (
                not fields_dict[field]['always_hidden']['detail']):
            self.assertIsNotNone(response.data.get(field), msg=msg)
        else:
            self.assertIsNone(response.data.get(field), msg=msg)

        response = self.client.get(
            reverse(self.rev_urls['list']), format='json'
        )
        user_data = list(filter(lambda item: item['id'] == user.pk, response.data['results']))[0]
        if is_visible and (
                not fields_dict[field]['always_hidden']['list']):
            self.assertIsNotNone(user_data.get(field), msg=msg)
        else:
            self.assertIsNone(user_data.get(field), msg=msg)

    def _get_user_and_set_settings(self, is_visible=False):
        user: User = User.objects.create_user(**self.data['user_01'])
        user.settings.email_visible = is_visible
        user.settings.watchlist_visible = is_visible
        user.settings.achievements_visible = is_visible
        user.settings.save()
        return user

    def helper_test_opt_hidden_fields_access(self, is_visible, msg):
        user = self._get_user_and_set_settings(is_visible)
        for field in self.OPTIONALLY_HIDDEN_FIELDS.keys():
            with self.subTest(field=field, is_visible=is_visible),\
                    transaction.atomic():
                self.helper_test_hidden_field(
                    field, self.OPTIONALLY_HIDDEN_FIELDS,
                    is_visible=is_visible, user=user, client=self.user,
                    msg=msg % (field, field)
                )
                transaction.set_rollback(True)

    def test_optionally_hidden_fields_access(self):
        with transaction.atomic():
            self.helper_test_opt_hidden_fields_access(
                False,
                'Field %s should not be visible for regular user'
                ' if user.settings.%s_visible is false'
            )
            transaction.set_rollback(True)
        with transaction.atomic():
            self.helper_test_opt_hidden_fields_access(
                True,
                'Field %s should be visible for regular user'
                ' if user.settings.%s_visible is true'
            )
            transaction.set_rollback(True)
