from django.urls import reverse

from rest_framework import status

from movie_service.models import PersonRequest, Person, PersonSubmission, Country

from . import AbstractApiModelTests


class ApiPersonRequestTests(AbstractApiModelTests):
    rev_urls = {
        'list': 'person_request-list',
        'detail': 'person_request-detail',
        'accept': 'person_request-accept',
        'reject': 'person_request-reject',
    }
    data = {
        'person_request_add_01': {
            'action': PersonRequest.ACTION_ADD,
            'header': 'What about Morgan Freeman?',
            'person_submission': {
                'name': 'Morgan',
                'surname': 'Freeman',
                'birthdate': '1965-03-22',
            },
        },
        'person_request_add_02': {
            'action': PersonRequest.ACTION_ADD,
            'header': 'What about Jodie Comer?',
            'person_submission': {
                'name': 'Jodie',
                'surname': 'Comer',
            },
        },
        'person_request_edit_01': {
            'action': PersonRequest.ACTION_EDIT,
            'header': "Freeman's birthdate is wrong!",
            'person_submission': {
                'name': 'Morgan',
                'surname': 'Freeman',
                'birthdate': '1937-06-01',
            },
        },
        'person_request_remove_01': {
            'action': PersonRequest.ACTION_REMOVE,
            'header': "It's a duplicate",
        },
        'country_01': {
            'name': 'United Kingdom',
            'short_name': 'UK'
        },
        'accept_01': {
            'details': 'Cuz I like it',
        },
        'reject_01': {
            'details': 'Cuz I hate it',
        }
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        p_sub = cls.data['person_request_add_01']['person_submission']
        p_sub['country'] = Country.objects.create(**cls.data['country_01']).pk

    def _create_pr(self, data=None):
        if data is None:
            data = self.data['person_request_add_01']
        data = data.copy()
        data['user'] = self.user
        if 'person_submission' in data:
            del data['person_submission']
        return PersonRequest.objects.create(**data)

    def _create_person(self, person_data=None, create_submission=False, pr=None):
        if person_data is None:
            person_data = self.data['person_request_add_01']['person_submission']
        data = person_data.copy()
        if create_submission:
            person_class = PersonSubmission
            data['person_request'] = pr
        else:
            person_class = Person
        if data.get('country') is not None:
            data['country'] = Country.objects.get(pk=data['country'])
        return person_class.objects.create(**data)

    def test_create_add_request(self):
        self.client.force_authenticate(self.root)
        data = self.data['person_request_add_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pr = PersonRequest.objects.get(pk=response.data['id'])
        self.assertEqual(pr.action, PersonRequest.ACTION_ADD)
        self.assertIsNone(pr.current_person)
        self.assertIsNotNone(pr.person_submission)

    def test_create_add_request_fail(self):
        self.client.force_authenticate(self.root)

        data = self.data['person_request_add_01'].copy()
        del data['person_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field person_submission should be required'
        )

        person = self._create_person()
        data = self.data['person_request_add_01'].copy()
        data['current_person'] = person.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_person should be blank'
        )

    def test_create_edit_request(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_edit_01'].copy()
        data['current_person'] = person.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pr = PersonRequest.objects.get(pk=response.data['id'])
        self.assertEqual(pr.action, PersonRequest.ACTION_EDIT)
        self.assertIsNotNone(pr.current_person)
        self.assertIsNotNone(pr.person_submission)
        self.assertEqual(pr.current_person_id, person.id)
        self.assertNotEqual(pr.person_submission.birthdate, person.birthdate)

    def test_create_edit_request_fail(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_edit_01'].copy()
        data['current_person'] = person.pk

        temp_data = data.copy()
        del temp_data['person_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field person_submission should be required'
        )

        temp_data = data.copy()
        del temp_data['current_person']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_person should be required'
        )

        temp_data = data.copy()
        del temp_data['person_submission']
        del temp_data['current_person']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Both fields person_submission, current_person should be required'
        )

    def test_create_remove_request(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_remove_01'].copy()
        data['current_person'] = person.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pr = PersonRequest.objects.get(pk=response.data['id'])
        self.assertEqual(pr.action, PersonRequest.ACTION_REMOVE)
        self.assertIsNotNone(pr.current_person)
        self.assertFalse(hasattr(pr, 'person_submission'))
        self.assertEqual(pr.current_person_id, person.id)

    def test_create_remove_request_fail(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_remove_01'].copy()
        data['current_person'] = person.pk

        temp_data = data.copy()
        del temp_data['current_person']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_person should be required'
        )

        temp_data = data.copy()
        data_person = self.data['person_request_add_01']['person_submission'].copy()
        temp_data['person_submission'] = data_person
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field person_submission should be blank'
        )

    def test_delete(self):
        self.client.force_authenticate(self.root)
        pr = self._create_pr()
        self._create_person(create_submission=True, pr=pr)
        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': pr.pk}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        pr = PersonRequest.objects.filter(pk=pr.pk).first()
        self.assertEqual(pr, None, msg='Request is still in the database')

    def test_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Person request update should not be allowed'
        )

    def test_partial_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Person request partial update should not be allowed'
        )

    def test_accept(self):
        self.client.force_authenticate(self.root)
        pr = self._create_pr()
        self._create_person(create_submission=True, pr=pr)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': pr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        pr.refresh_from_db()
        self.assertEqual(
            pr.status, PersonRequest.STATUS_ACCEPTED,
            msg='Person request should be accepted'
        )
        self.assertIsNotNone(
            pr.requestlog_set.first(),
            msg='Person request accept should be logged'
        )
        self.assertEqual(
            pr.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Person request accept log should be associated with '
                'the user who accepted it'
        )

    def test_accept_add(self):
        self.client.force_authenticate(self.root)
        pr = self._create_pr()
        self._create_person(create_submission=True, pr=pr)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': pr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        new_person = Person.objects.filter(
            name=pr.person_submission.name, surname=pr.person_submission.surname
        ).first()
        self.assertIsNotNone(
            new_person,
            msg='New Person should be created based on the submission'
        )

    def test_accept_edit(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_edit_01'].copy()
        data['user'] = self.user
        data['current_person'] = person
        pr = self._create_pr(data)
        self._create_person(
            data['person_submission'], create_submission=True, pr=pr
        )

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': pr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        # well, without it pr.person_submission.birthdate is a string...
        pr.refresh_from_db()
        person.refresh_from_db()
        self.assertEqual(
            person.birthdate, pr.person_submission.birthdate,
            msg='Person birthdate should be updated based on the submission'
        )
        self.assertIsNone(
            person.country,
            msg='Person country should be null '
                'cuz it was not provided in the submission'
        )

    def test_accept_remove(self):
        self.client.force_authenticate(self.root)
        person = self._create_person()
        data = self.data['person_request_remove_01'].copy()
        data['user'] = self.user
        data['current_person'] = person
        pr = self._create_pr(data)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': pr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        removed_person = Person.objects.filter(pk=person.pk).first()
        self.assertIsNone(
            removed_person,
            msg='Person should be removed'
        )
        self.assertIsNotNone(
            PersonRequest.objects.filter(pk=pr.pk).first(),
            msg='Person request should still exist after removing the Person'
        )

    def test_reject(self):
        self.client.force_authenticate(self.root)
        pr = self._create_pr()
        self._create_person(create_submission=True, pr=pr)

        data = self.data['reject_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': pr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        pr.refresh_from_db()
        self.assertEqual(
            pr.status, PersonRequest.STATUS_REJECTED,
            msg='Person request should be rejected'
        )
        self.assertIsNotNone(
            pr.requestlog_set.first(),
            msg='Person request reject should be logged'
        )
        self.assertEqual(
            pr.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Person request reject log should be associated with '
                'the user who rejected it'
        )
