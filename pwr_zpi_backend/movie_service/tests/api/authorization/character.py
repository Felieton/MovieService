from django.urls import reverse

from rest_framework import status

from movie_service.models import Character, Person

from . import AbstractApiModelAuthTests


class ApiCharacterAuthTests(AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'character-list',
        'detail': 'character-detail',
    }
    data = {
        'character_01': {
            'name': 'God',
        },
        'character_02': {
            'name': 'Devil',
        },
        'person_01': {
            'name': 'Morgan',
            'surname': 'Freeman',
        },
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
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

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        person = Person.objects.create(**self.data['person_01'])
        data = self.data['character_01'].copy()
        data['person'] = person.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_create_access(self):
        self.helper_test_general_access(
            self.actions_tests['create'],
            self.helper_test_create_access
        )

    def helper_test_delete_access(self, user, expected_status):
        self.client.force_authenticate(user)
        person = Person.objects.create(**self.data['person_01'])
        new_character = Character.objects.create(person_id=person.pk, **self.data['character_01'])
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_character.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_delete_access(self):
        self.helper_test_general_access(
            self.actions_tests['delete'],
            self.helper_test_delete_access
        )

    def helper_test_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        person = Person.objects.create(**self.data['person_01'])
        new_character = Character.objects.create(person_id=person.pk, **self.data['character_01'])
        modified_character = self.data['character_01'].copy()
        modified_character['name'] = self.data['character_02']['name']
        modified_character['person'] = person.pk
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_character.pk}),
            data=modified_character, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['update'],
            self.helper_test_update_access
        )

    def helper_test_partial_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        person = Person.objects.create(**self.data['person_01'])
        new_character = Character.objects.create(person_id=person.pk, **self.data['character_01'])
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_character.pk}),
            data={'name': self.data['character_02']['name']}, format='json'
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
        person = Person.objects.create(**self.data['person_01'])
        new_character = Character.objects.create(person_id=person.pk, **self.data['character_01'])
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_character.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )
