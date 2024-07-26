from django.urls import reverse

from movie_service.models import TitleRequest, TitleSubmission

from . import AbstractApiModelAuthTests, RequestPermissionsMixin


class ApiTitleRequestAuthTests(RequestPermissionsMixin,
                               AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'title_request-list',
        'detail': 'title_request-detail',
        'accept': 'title_request-accept',
        'reject': 'title_request-reject',
    }
    data = {
        'title_request_01': {
            'action': TitleRequest.ACTION_ADD,
            'header': 'What about The Wheel of Time?',
            'title_submission': {
                "title": "The Wheel of Time",
                "type": TitleSubmission.TYPE_SERIES,
            },
        },
        'accept_01': {
            'details': 'I like snow',
        },
        'reject_01': {
            'details': 'Windows 11 has been released',
        }
    }

    def _create_tr_submission(self, tr):
        data = self.data['title_request_01']['title_submission'].copy()
        data['title_request'] = tr
        return TitleSubmission.objects.create(**data)

    def _create_tr(self):
        data = self.data['title_request_01'].copy()
        data['user'] = self.user
        del data['title_submission']
        tr = TitleRequest.objects.create(**data)
        self._create_tr_submission(tr)
        return tr

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        data = self.data['title_request_01'].copy()
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
        tr = self._create_tr()
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': tr.pk}), format='json'
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
        tr = self._create_tr()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': tr.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )

    def helper_test_accept_access(self, user, expected_status):
        self.client.force_authenticate(user)
        tr = self._create_tr()
        data = self.data['accept_01']
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': tr.pk}),
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
        tr = self._create_tr()
        data = self.data['reject_01']
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': tr.pk}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_reject_access(self):
        self.helper_test_general_access(
            self.actions_tests['reject'],
            self.helper_test_reject_access
        )
