from django.urls import reverse

from movie_service.models import PersonRequest, PersonSubmission

from . import AbstractApiModelAuthTests, RequestPermissionsMixin


class ApiPersonRequestAuthTests(RequestPermissionsMixin,
                                AbstractApiModelAuthTests):
    rev_urls = {
        'list': 'person_request-list',
        'detail': 'person_request-detail',
        'accept': 'person_request-accept',
        'reject': 'person_request-reject',
    }
    data = {
        'person_request_01': {
            'action': PersonRequest.ACTION_ADD,
            'header': 'What about Morgan Freeman?',
            'person_submission': {
                "name": "Morgan",
                "surname": "Freeman",
            },
        },
        'accept_01': {
            'details': 'I like snow',
        },
        'reject_01': {
            'details': 'Windows 11 has been released',
        }
    }

    def _create_pr_submission(self, pr):
        data = self.data['person_request_01']['person_submission'].copy()
        data['person_request'] = pr
        return PersonSubmission.objects.create(**data)

    def _create_pr(self):
        data = self.data['person_request_01'].copy()
        data['user'] = self.user
        del data['person_submission']
        pr = PersonRequest.objects.create(**data)
        self._create_pr_submission(pr)
        return pr

    def helper_test_create_access(self, user, expected_status):
        self.client.force_authenticate(user)
        data = self.data['person_request_01'].copy()
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
        new_person_request = self._create_pr()
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_person_request.pk}), format='json'
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
        new_person_request = self._create_pr()
        response = self.client.get(
            reverse(self.rev_urls['detail'], kwargs={'pk': new_person_request.pk}), format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_retrieve_access(self):
        self.helper_test_general_access(
            self.actions_tests['retrieve'],
            self.helper_test_retrieve_access
        )

    def helper_test_accept_access(self, user, expected_status):
        self.client.force_authenticate(user)
        pr = self._create_pr()
        data = self.data['accept_01']
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': pr.pk}),
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
        pr = self._create_pr()
        data = self.data['reject_01']
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': pr.pk}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, expected_status)

    def test_reject_access(self):
        self.helper_test_general_access(
            self.actions_tests['reject'],
            self.helper_test_reject_access
        )
