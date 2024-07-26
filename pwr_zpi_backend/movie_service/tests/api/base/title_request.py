from functools import reduce

from django.urls import reverse

from rest_framework import status

from movie_service.models import TitleRequest, TitleSubmission, Title, \
    RequestLog

from . import AbstractApiModelTests, TitleTestsMixin


class ApiTitleRequestTests(TitleTestsMixin, AbstractApiModelTests):
    rev_urls = {
        'list': 'title_request-list',
        'detail': 'title_request-detail',
        'accept': 'title_request-accept',
        'reject': 'title_request-reject',
    }
    data = {
        'title_request_add_01': {
            'action': TitleRequest.ACTION_ADD,
            'header': 'What about Se7en?',
            'title_submission': {
                'title': 'Se7en',
                'year': 1995,
                'released': '1995-09-22',
                'type': TitleSubmission.TYPE_MOVIE,
                'languages': [7, 11, 13, 17, 19],
                'countries': [9, 9, 7],
                'genres': [1, 3, 7, 11],
                'characters': [
                    {
                        'name': 'Somerset',
                        'person': 6,
                    },
                    {
                        'name': 'Mills',
                        'person': 16,
                    },
                ],
                'cast_members': [
                    {
                        'person': 3,
                        'roles': [1, 5, 2]
                    },
                    {
                        'person': 23,
                        'roles': [5, 9, 4]
                    },
                ]
            },
        },
        'title_request_edit_01': {
            'action': TitleRequest.ACTION_EDIT,
            'header': "Release date is wrong",
            'title_submission': {
                'title': 'The Wheel of Time',
                'year': 2021,
                'released': '2021-11-19',
                'type': TitleSubmission.TYPE_SERIES,
                'languages': [1, 1, 2],
                'countries': [9, 1, 1],
                'genres': [9, 9, 7],
                'characters': [
                    {
                        'name': 'Moraine',
                        'person': 6,
                    },
                    {
                        'name': 'Egwene',
                        'person': 21,
                    },
                ],
                'cast_members': [
                    {
                        'person': 3,
                        'roles': [11, 16, 19]
                    },
                    {
                        'person': 8,
                        'roles': [5, 9, 4]
                    },
                ]
            },
        },
        'title_request_remove_01': {
            'action': TitleRequest.ACTION_REMOVE,
            'header': "It's a duplicate",
        },
        'accept_01': {
            'details': 'Cuz I like it',
        },
        'reject_01': {
            'details': 'Cuz I hate it',
        }
    }

    def _create_log(self, title_request):
        log_data = {
            'details': 'Request processed',
            'title_request': title_request,
            'moderator': self.root,
        }
        return RequestLog.objects.create(**log_data)

    @classmethod
    def _get_title_data_no_m2m(cls, title_data=None):
        if title_data is None:
            title_data = cls.data['title_request_add_01']['title_submission']
        return super()._get_title_data_no_m2m(title_data)

    @classmethod
    def _create_title_with_m2m(cls, title_data=None, create_submission=False, tr=None):
        if title_data is None:
            title_data = cls.data['title_request_add_01']['title_submission']
        return super()._create_title_with_m2m(title_data, create_submission, tr)

    def _create_request_with_m2m(self, request_data=None):
        if request_data is None:
            request_data = self.data['title_request_add_01']
        data = request_data.copy()
        data['user'] = self.user
        tr_sub_data = None
        if 'title_submission' in data:
            tr_sub_data = data['title_submission']
            del data['title_submission']
        tr = TitleRequest.objects.create(**data)
        self._create_title_with_m2m(tr_sub_data, True, tr)
        return tr

    def test_create_add_request(self):
        self.client.force_authenticate(self.root)
        data = self.data['title_request_add_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        tr = TitleRequest.objects.get(pk=response.data['id'])
        self.assertEqual(tr.action, TitleRequest.ACTION_ADD)
        self.assertIsNone(tr.current_title)
        self.assertIsNotNone(tr.title_submission)
        tr_sub = tr.title_submission
        self.assertEqual(tr_sub.title, data['title_submission']['title'])
        self.assertEqual(tr_sub.year, data['title_submission']['year'])
        self.assertEqual(tr_sub.released.isoformat(), data['title_submission']['released'])
        self.assertEqual(tr_sub.type, data['title_submission']['type'])
        match_attrs_by_id = ['languages', 'countries', 'genres']
        for attr in match_attrs_by_id:
            qs1 = getattr(tr_sub, attr)
            self.assertEqual(
                set(map(lambda item: item['id'], qs1.values('id'))),
                set(data['title_submission'][attr]),
                msg=f"Submission's {attr} set should match provided data set"
            )
        self.assertEqual(
            sorted(tr_sub.characters.values('name', 'person'), key=lambda item: item.get('name')),
            sorted(data['title_submission']['characters'], key=lambda item: item.get('name'))
        )
        self.assertEqual(
            tr_sub.cast_members.values('person', 'roles').count(),
            reduce(
                lambda a, b: len(set(a['roles'])) + len(set(b['roles'])),
                data['title_submission']['cast_members']
            ),
        )

    def test_create_add_request_fail(self):
        self.client.force_authenticate(self.root)

        data = self.data['title_request_add_01'].copy()
        del data['title_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field title_submission should be required'
        )

        data_title_no_m2m = self._get_title_data_no_m2m()
        title = Title.objects.create(**data_title_no_m2m)
        data = self.data['title_request_add_01'].copy()
        data['title_submission'] = data_title_no_m2m
        data['current_title'] = title.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_title should be blank'
        )

    def test_create_edit_request(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_edit_01'].copy()
        data['current_title'] = title.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tr = TitleRequest.objects.get(pk=response.data['id'])
        self.assertEqual(tr.action, TitleRequest.ACTION_EDIT)
        self.assertIsNotNone(tr.current_title)
        self.assertIsNotNone(tr.title_submission)
        self.assertEqual(tr.current_title_id, title.id)
        self.assertNotEqual(tr.title_submission.title, title.title)

    def test_create_edit_request_fail(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_edit_01'].copy()
        data['current_title'] = title.pk

        temp_data = data.copy()
        del temp_data['title_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field title_submission should be required'
        )

        temp_data = data.copy()
        del temp_data['current_title']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_title should be required'
        )

        temp_data = data.copy()
        del temp_data['title_submission']
        del temp_data['current_title']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Both fields title_submission, current_title should be required'
        )

    def test_create_remove_request(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_remove_01'].copy()
        data['current_title'] = title.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tr = TitleRequest.objects.get(pk=response.data['id'])
        self.assertEqual(tr.action, TitleRequest.ACTION_REMOVE)
        self.assertIsNotNone(tr.current_title)
        self.assertFalse(hasattr(tr, 'title_submission'))
        self.assertEqual(tr.current_title_id, title.id)

    def test_create_remove_request_fail(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_remove_01'].copy()
        data['current_title'] = title.pk

        temp_data = data.copy()
        del temp_data['current_title']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_title should be required'
        )

        temp_data = data.copy()
        temp_data['title_submission'] = self._get_title_data_no_m2m()
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field title_submission should be blank'
        )

    def test_delete(self):
        self.client.force_authenticate(self.root)
        tr = self._create_request_with_m2m()
        self._create_log(tr)

        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': tr.pk}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tr = TitleRequest.objects.filter(pk=tr.pk).first()
        self.assertEqual(tr, None, msg='Request is still in the database')

    def test_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Title request update should not be allowed'
        )

    def test_partial_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Title request partial update should not be allowed'
        )

    def test_accept(self):
        self.client.force_authenticate(self.root)
        tr = self._create_request_with_m2m()

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': tr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        tr.refresh_from_db()
        self.assertEqual(
            tr.status, TitleRequest.STATUS_ACCEPTED,
            msg='Title request should be accepted'
        )
        self.assertIsNotNone(
            tr.requestlog_set.first(),
            msg='Title request accept should be logged'
        )
        self.assertEqual(
            tr.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Title request accept log should be associated with '
                'the user who accepted it'
        )

    def test_accept_add(self):
        self.client.force_authenticate(self.root)
        tr = self._create_request_with_m2m()

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': tr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        new_title = Title.objects.filter(
            title=tr.title_submission.title, year=tr.title_submission.year
        ).first()
        self.assertIsNotNone(
            new_title,
            msg='New Title should be created based on the submission'
        )
        match_attrs_by_id = ['languages', 'countries', 'genres', 'characters', 'cast_members']
        for attr in match_attrs_by_id:
            qs1 = getattr(tr.title_submission, attr)
            qs2 = getattr(new_title, attr)
            self.assertEqual(
                set(map(lambda item: item['id'], qs1.values('id'))),
                set(map(lambda item: item['id'], qs2.values('id'))),
                msg=f"Submission's {attr} set should match Title's "
                    f"after successful create"
            )

        '''
        print(tr.title_submission.languages.values('id', 'name'))
        print(new_title.languages.values('id', 'name'))

        print(tr.title_submission.countries.values('id', 'short_name'))
        print(new_title.countries.values('id', 'short_name'))

        print(tr.title_submission.genres.values('id', 'name'))
        print(new_title.genres.values('id', 'name'))

        print(tr.title_submission.characters.values('id', 'name', 'person'))
        print(new_title.characters.values('id', 'name', 'person'))

        print(tr.title_submission.cast_members.values('id', 'person'))
        print(new_title.cast_members.values('id', 'person'))
        '''

    def test_accept_edit(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_edit_01'].copy()
        data['current_title'] = title
        tr = self._create_request_with_m2m(data)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': tr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        tr.refresh_from_db()
        title.refresh_from_db()
        self.assertEqual(
            title.title, tr.title_submission.title,
            msg='Title\'s title should be updated based on the submission'
        )
        match_attrs_by_id = ['languages', 'countries', 'genres', 'characters', 'cast_members']
        for attr in match_attrs_by_id:
            qs1 = getattr(tr.title_submission, attr)
            qs2 = getattr(title, attr)
            self.assertEqual(
                set(map(lambda item: item['id'], qs1.values('id'))),
                set(map(lambda item: item['id'], qs2.values('id'))),
                msg=f"Submission's {attr} set should match Title's "
                    f"after successful edit"
            )

        '''
        print(tr.title_submission.languages.values('id', 'name'))
        print(title.languages.values('id', 'name'))

        print(tr.title_submission.countries.values('id', 'short_name'))
        print(title.countries.values('id', 'short_name'))

        print(tr.title_submission.genres.values('id', 'name'))
        print(title.genres.values('id', 'name'))

        characters_all = Character.objects.all()
        print(tr.title_submission.characters.values('id', 'name', 'person'))
        print(title.characters.values('id', 'name', 'person'))

        cm_all = CastMember.objects.all()
        print(tr.title_submission.cast_members.values('id', 'person'))
        print(title.cast_members.values('id', 'person'))
        print('end')
        '''

    def test_accept_remove(self):
        self.client.force_authenticate(self.root)
        title = self._create_title_with_m2m()
        data = self.data['title_request_remove_01'].copy()
        data['user'] = self.user
        data['current_title'] = title
        tr = TitleRequest.objects.create(**data)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': tr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        removed_title = Title.objects.filter(pk=title.pk).first()
        self.assertIsNone(
            removed_title,
            msg='Title should be removed'
        )
        self.assertIsNotNone(
            TitleRequest.objects.filter(pk=tr.pk).first(),
            msg='Title request should still exist after removing the Title'
        )

    def test_reject(self):
        self.client.force_authenticate(self.root)
        tr = self._create_request_with_m2m()

        data = self.data['reject_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': tr.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        tr.refresh_from_db()
        self.assertEqual(
            tr.status, TitleRequest.STATUS_REJECTED,
            msg='Title request should be rejected'
        )
        self.assertIsNotNone(
            tr.requestlog_set.first(),
            msg='Title request reject should be logged'
        )
        self.assertEqual(
            tr.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Title request reject log should be associated with '
                'the user who rejected it'
        )
