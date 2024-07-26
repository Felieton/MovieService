from django.urls import reverse

from rest_framework import status

from movie_service.models import Episode, Title

from . import AbstractApiModelAuthTests


class ApiEpisodeAuthTests(AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'episode-list',
        'detail': 'episode-detail',
    }
    data = {
        'object': {
            'name': "The Dragon Reborn",
            'title': 1,
            'number': 4,
            'season': 1,
        },
        'object_02': {
            'name': "Who cares",
        },
        'title_01': {
            "title": "The Wheel of Time",
            "type": Title.TYPE_SERIES,
            'seasons_count': 1,
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_201_CREATED),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'delete': [
                (cls.root, status.HTTP_204_NO_CONTENT),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'update': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_403_FORBIDDEN),
                (cls.moderator, status.HTTP_403_FORBIDDEN),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'partial_update': [
                (cls.root, status.HTTP_200_OK),
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
        cls.title = Title.objects.create(**cls.data['title_01'])
        data = cls.data['object']
        data['title'] = cls.title.pk

    def _create_episode(self):
        data = self.data['object'].copy()
        data['title'] = self.title
        return Episode.objects.create(**data)

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
        new_object = self._create_episode()
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
        new_object = self._create_episode()
        modified_object = self.data['object'].copy()
        modified_object['name'] = self.data['object_02']['name']
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
        new_object = self._create_episode()
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}),
            data={'name': self.data['object_02']['name']}, format='json'
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
        new_object = self._create_episode()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )
