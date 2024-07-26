from django.urls import reverse

from rest_framework import status

from movie_service.models import Review, Title, User

from . import AbstractApiModelAuthTests


class ApiAuthReviewTests(AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'review-list',
        'detail': 'review-detail',
        'accept': 'review-accept',
        'reject': 'review-reject',
    }
    data = {
        'object': {
            'header': "It's such a great show",
            'body': 'Lorem ipsum dolor sit amet',
            'rating': 8,
        },
        'object_02': {
            'header': "I hate it",
        },
        'title_01': {
            "title": "The Wheel of Time",
            "type": Title.TYPE_SERIES,
            'seasons_count': 1,
        },
        'user_01': {
            'username': 'testuser01',
            'email': 'testuser01@example.com',
            'password': 'TestUser01P@ss!'
        },
        'accept_01': {
            'details': 'I like snow',
        },
        'reject_01': {
            'details': 'Windows 11 has been released',
        }
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_201_CREATED),
                (cls.admin, status.HTTP_201_CREATED),
                (cls.moderator, status.HTTP_201_CREATED),
                (cls.user, status.HTTP_201_CREATED),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'delete': [
                (cls.root, status.HTTP_204_NO_CONTENT),
                (cls.admin, status.HTTP_204_NO_CONTENT),
                (cls.moderator, status.HTTP_204_NO_CONTENT),
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
            'accept': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'reject': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ]
        }
        cls.title = Title.objects.create(**cls.data['title_01'])
        data = cls.data['object']
        data['title'] = cls.title.pk
        cls.user = User.objects.create(**cls.data['user_01'])

    @classmethod
    def _create_review(cls):
        review_data = cls.data['object']
        data = review_data.copy()
        data['user'] = cls.user
        data['title'] = cls.title
        return Review.objects.create(**data)

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
        new_object = self._create_review()
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
        new_object = self._create_review()
        modified_object = self.data['object'].copy()
        modified_object['header'] = self.data['object_02']['header']
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
        new_object = self._create_review()
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}),
            data={'header': self.data['object_02']['header']}, format='json'
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
        new_object = self._create_review()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )

    def helper_test_accept_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_object = self._create_review()
        data = self.data['accept_01']
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': new_object.pk}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_accept_access(self):
        self.helper_test_general_access(
            self.actions_tests['accept'],
            self.helper_test_accept_access
        )

    def helper_test_reject_access(self, user, expected_status):
        self.client.force_authenticate(user)
        new_object = self._create_review()
        data = self.data['reject_01']
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': new_object.pk}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_reject_access(self):
        self.helper_test_general_access(
            self.actions_tests['reject'],
            self.helper_test_reject_access
        )

    def test_owner_delete_access(self):
        self.client.force_authenticate(self.user)
        data = self.data['object'].copy()
        data['user'] = self.user
        data['title'] = self.title
        new_object = Review.objects.create(**data)
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_object.pk}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
