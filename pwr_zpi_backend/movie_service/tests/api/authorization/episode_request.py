from django.urls import reverse

from movie_service.models import EpisodeRequest, EpisodeSubmission, Title

from . import AbstractApiModelAuthTests, RequestPermissionsMixin


class ApiEpisodeRequestAuthTests(RequestPermissionsMixin,
                                 AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'episode_request-list',
        'detail': 'episode_request-detail',
        'accept': 'episode_request-accept',
        'reject': 'episode_request-reject',
    }
    data = {
        'episode_request_01': {
            'action': EpisodeRequest.ACTION_ADD,
            'header': 'What about The Wheel of Time?',
            'episode_submission': {
                'name': "The Dragon Reborn",
                'title': 1,
                'number': 4,
                'season': 1,
            },
        },
        'accept_01': {
            'details': 'I like snow',
        },
        'reject_01': {
            'details': 'Windows 11 has been released',
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
        cls.title = Title.objects.create(**cls.data['title_01'])
        data = cls.data['episode_request_01']['episode_submission']
        data['title'] = cls.title.pk

    def _create_er_submission(self, er):
        data = self.data['episode_request_01']['episode_submission'].copy()
        data['title'] = self.title
        data['episode_request'] = er
        return EpisodeSubmission.objects.create(**data)

    def _create_er(self):
        data = self.data['episode_request_01'].copy()
        data['user'] = self.user
        del data['episode_submission']
        er = EpisodeRequest.objects.create(**data)
        self._create_er_submission(er)
        return er

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        data = self.data['episode_request_01'].copy()
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
        er = self._create_er()
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': er.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_delete_access(self):
        self.helper_test_general_access(
            self.actions_tests['delete'],
            self.helper_test_delete_access
        )

    def helper_test_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}),
            data={}, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_update_access(self):
        self.helper_test_general_access(
            self.actions_tests['update'],
            self.helper_test_update_access
        )

    def helper_test_partial_update_access(self, user, expected_status):
        self.client.force_authenticate(user)
        response = self.client.patch(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}),
            data={}, format='json'
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
        er = self._create_er()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': er.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )

    def helper_test_accept_access(self, user, expected_status):
        self.client.force_authenticate(user)
        er = self._create_er()
        data = self.data['accept_01']
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': er.pk}),
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
        er = self._create_er()
        data = self.data['reject_01']
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': er.pk}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_reject_access(self):
        self.helper_test_general_access(
            self.actions_tests['reject'],
            self.helper_test_reject_access
        )
