from django.urls import reverse

from rest_framework import status

from movie_service.models import CastRole

from . import AbstractApiModelAuthTests


class ApiCastRoleAuthTests(AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'cast_role-list',
        'detail': 'cast_role-detail',
    }
    data = {
        'cast_role_01': {
            'name': 'director',
        },
        'cast_role_02': {
            'name': 'writer',
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_201_CREATED),
                (cls.admin, status.HTTP_201_CREATED),
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
            reverse(self.rev_urls['list']), self.data['cast_role_01'], format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_create_access(self):
        self.helper_test_general_access(
            self.actions_tests['create'],
            self.helper_test_create_access
        )

    def helper_test_delete_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_cast_role = CastRole.objects.create(**self.data['cast_role_01'])
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_cast_role.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_delete_access(self):
        self.helper_test_general_access(
            self.actions_tests['delete'],
            self.helper_test_delete_access
        )

    def helper_test_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_cast_role = CastRole.objects.create(**self.data['cast_role_01'])
        modified_cast_role = self.data['cast_role_01'].copy()
        modified_cast_role['name'] = self.data['cast_role_02']['name']
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_cast_role.pk}),
            data=modified_cast_role, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['update'],
            self.helper_test_update_access
        )

    def helper_test_partial_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_cast_role = CastRole.objects.create(**self.data['cast_role_01'])
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_cast_role.pk}),
            data={'name': self.data['cast_role_02']['name']}, format='json'
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
        new_cast_role = CastRole.objects.create(**self.data['cast_role_01'])
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_cast_role.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )
