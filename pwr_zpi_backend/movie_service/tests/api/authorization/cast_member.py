from django.urls import reverse

from rest_framework import status

from movie_service.models import CastMember, Person

from .. import init_title_related_simple_objects
from . import AbstractApiModelAuthTests


class ApiCastMemberAuthTests(AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'cast_member-list',
        'detail': 'cast_member-detail',
    }
    data = {
        'object': {
            'person': 1,
            'roles': [1, 3, 7],
        },
        'object_02': {
            'roles': [9, 11, 15],
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        init_title_related_simple_objects()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'delete': [
                (cls.root, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'update': [
                (cls.root, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'partial_update': [
                (cls.root, status.HTTP_405_METHOD_NOT_ALLOWED),
                (cls.admin, status.HTTP_403_FORBIDDEN),
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

    def _create_cast_member(self):
        data = self.data['object'].copy()
        data['person'] = Person.objects.get(pk=data['person'])
        roles = data['roles']
        del data['roles']
        cm = CastMember.objects.create(**data)
        cm.roles.set(roles)
        return cm

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse(self.rev_urls['list']), self.data['object'], format='json'
        )
        self.assertEqual(response.status_code, expected_status, msg=response.data)

    def test_create_access(self):
        self.helper_test_general_access(
            self.actions_tests['create'],
            self.helper_test_create_access
        )

    def helper_test_delete_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_object = self._create_cast_member()
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_delete_access(self):
        self.helper_test_general_access(
            self.actions_tests['delete'],
            self.helper_test_delete_access
        )

    def helper_test_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_object = self._create_cast_member()
        modified_object = self.data['object'].copy()
        modified_object['roles'] = self.data['object_02']['roles']
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}),
            data=modified_object, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['update'],
            self.helper_test_update_access
        )

    def helper_test_partial_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_object = self._create_cast_member()
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}),
            data={'roles': self.data['object_02']['roles']}, format='json'
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
        new_object = self._create_cast_member()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )
