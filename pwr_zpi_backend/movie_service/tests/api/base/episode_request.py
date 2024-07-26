from django.urls import reverse

from rest_framework import status

from movie_service.models import EpisodeRequest, EpisodeSubmission, Title, \
    Episode, RequestLog

from . import AbstractApiModelTests, TitleTestsMixin


class ApiEpisodeRequestTests(TitleTestsMixin, AbstractApiModelTests):
    rev_urls = {
        'list': 'episode_request-list',
        'detail': 'episode_request-detail',
        'accept': 'episode_request-accept',
        'reject': 'episode_request-reject',
    }
    data = {
        'episode_request_add_01': {
            'action': EpisodeRequest.ACTION_ADD,
            'header': 'What about first episode?',
            'episode_submission': {
                'name': 'Leavetaking',
                'released': '2021-11-19',
                'season': 1,
                'number': 1,
                'title': 1,
                'characters': [1, 2],
            },
        },
        'episode_request_edit_01': {
            'action': EpisodeRequest.ACTION_EDIT,
            'header': "Some info is just plain wrong",
            'episode_submission': {
                'name': 'The Dragon Reborn',
                'released': '2021-11-26',
                'season': 1,
                'number': 4,
                'title': 1,
                'characters': [2, 3],
            },
        },
        'episode_request_remove_01': {
            'action': EpisodeRequest.ACTION_REMOVE,
            'header': "It's a duplicate",
        },
        'person_01': {
            'name': 'Morgan',
            'surname': 'Freeman',
            'birthdate': '1937-06-01',
        },
        'title_01': {
            'title': 'The Wheel of Time',
            'year': 2021,
            'released': '2021-11-19',
            'type': Title.TYPE_SERIES,
            'seasons_count': 1,
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
                {
                    'name': 'Lan Mandragoran',
                    'person': 25,
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

        title = cls._create_title_with_m2m()
        characters = title.as_dict()['characters']

        episode_sub = cls.data['episode_request_add_01']['episode_submission']
        episode_sub['title'] = title.pk
        episode_sub['characters'] = characters[:2]

        episode_sub = cls.data['episode_request_edit_01']['episode_submission']
        episode_sub['title'] = title.pk
        episode_sub['characters'] = characters[1:]

    def _create_log(self, episode_request):
        log_data = {
            'details': 'Request processed',
            'episode_request': episode_request,
            'moderator': self.root,
        }
        return RequestLog.objects.create(**log_data)

    @staticmethod
    def _get_sub_dict(dict_obj, keys):
        return {key: dict_obj[key] for key in keys}

    def _get_episode_sub_data_no_m2m(self):
        episode_data = self.data['episode_request_add_01']['episode_submission']
        data = episode_data.copy()
        no_m2m_keys = ['name', 'released', 'season', 'number', 'title']
        return self._get_sub_dict(data, no_m2m_keys)

    def _get_episode_data_no_rel(self, episode_data):
        data = episode_data.copy()
        no_rel_keys = ['name', 'released', 'season', 'number']
        return self._get_sub_dict(data, no_rel_keys)

    def _create_episode_with_m2m(self, episode_data=None, create_submission=False, er=None):
        if episode_data is None:
            episode_data = self.data['episode_request_add_01']['episode_submission']
        data = episode_data.copy()
        data_no_m2m = self._get_episode_data_no_rel(data)
        data_no_m2m['title'] = Title.objects.get(pk=data['title'])
        if create_submission:
            create_class = EpisodeSubmission
            data_no_m2m['episode_request'] = er
        else:
            create_class = Episode
        episode_obj = create_class.objects.create(**data_no_m2m)
        episode_obj.characters.set(data['characters'])

        return episode_obj

    def _create_request_with_m2m(self, request_data=None):
        if request_data is None:
            request_data = self.data['episode_request_add_01']
        data = request_data.copy()
        data['user'] = self.user
        er_sub_data = data['episode_submission']
        del data['episode_submission']
        er = EpisodeRequest.objects.create(**data)
        self._create_episode_with_m2m(
            er_sub_data, True, er
        )
        return er

    def test_create_add_request(self):
        self.client.force_authenticate(self.root)
        data = self.data['episode_request_add_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        er = EpisodeRequest.objects.get(pk=response.data['id'])
        self.assertEqual(er.action, EpisodeRequest.ACTION_ADD)
        self.assertIsNone(er.current_episode)
        self.assertIsNotNone(er.episode_submission)
        er_sub = er.episode_submission
        self.assertEqual(er_sub.name, data['episode_submission']['name'])
        self.assertEqual(er_sub.released.isoformat(), data['episode_submission']['released'])
        self.assertEqual(er_sub.season, data['episode_submission']['season'])
        self.assertEqual(er_sub.number, data['episode_submission']['number'])
        self.assertEqual(
            set(map(lambda item: item['id'], er_sub.characters.values('id'))),
            set(data['episode_submission']['characters']),
            msg=f"Submission's characters set should match provided data set"
        )

    def test_create_add_request_fail(self):
        self.client.force_authenticate(self.root)

        data = self.data['episode_request_add_01'].copy()
        del data['episode_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field episode_submission should be required'
        )

        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_add_01'].copy()
        data['current_episode'] = episode.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_episode should be blank'
        )

    def test_create_edit_request(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_edit_01'].copy()
        data['current_episode'] = episode.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        er = EpisodeRequest.objects.get(pk=response.data['id'])
        self.assertEqual(er.action, EpisodeRequest.ACTION_EDIT)
        self.assertIsNotNone(er.current_episode)
        self.assertIsNotNone(er.episode_submission)
        self.assertEqual(er.current_episode_id, episode.id)
        self.assertNotEqual(er.episode_submission.name, episode.name)

    def test_create_edit_request_fail(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_edit_01'].copy()
        data['current_episode'] = episode.pk

        temp_data = data.copy()
        del temp_data['episode_submission']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field episode_submission should be required'
        )

        temp_data = data.copy()
        del temp_data['current_episode']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_episode should be required'
        )

        temp_data = data.copy()
        del temp_data['episode_submission']
        del temp_data['current_episode']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Both fields episode_submission, current_episode should be required'
        )

    def test_create_remove_request(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_remove_01'].copy()
        data['current_episode'] = episode.pk
        response = self.client.post(
            reverse(self.rev_urls['list']), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        er = EpisodeRequest.objects.get(pk=response.data['id'])
        self.assertEqual(er.action, EpisodeRequest.ACTION_REMOVE)
        self.assertIsNotNone(er.current_episode)
        self.assertFalse(hasattr(er, 'episode_submission'))
        self.assertEqual(er.current_episode_id, episode.id)

    def test_create_remove_request_fail(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_remove_01'].copy()
        data['current_episode'] = episode.pk

        temp_data = data.copy()
        del temp_data['current_episode']
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field current_episode should be required'
        )

        temp_data = data.copy()
        temp_data['episode_submission'] = self._get_episode_sub_data_no_m2m()
        response = self.client.post(
            reverse(self.rev_urls['list']), temp_data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Field episode_submission should be blank'
        )

    def test_delete(self):
        self.client.force_authenticate(self.root)
        er = self._create_request_with_m2m()
        self._create_log(er)

        response = self.client.delete(
            reverse(self.rev_urls['detail'], kwargs={'pk': er.pk}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        er = EpisodeRequest.objects.filter(pk=er.pk).first()
        self.assertEqual(er, None, msg='Request is still in the database')

    def test_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Episode request update should not be allowed'
        )

    def test_partial_update(self):
        self.client.force_authenticate(self.root)
        response = self.client.put(
            reverse(self.rev_urls['detail'], kwargs={'pk': 404}), format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            msg='Episode request partial update should not be allowed'
        )

    def test_accept(self):
        self.client.force_authenticate(self.root)
        er = self._create_request_with_m2m()

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': er.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        er.refresh_from_db()
        self.assertEqual(
            er.status, EpisodeRequest.STATUS_ACCEPTED,
            msg='Episode request should be accepted'
        )
        self.assertIsNotNone(
            er.requestlog_set.first(),
            msg='Episode request accept should be logged'
        )
        self.assertEqual(
            er.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Episode request accept log should be associated with '
                'the user who accepted it'
        )

    def test_accept_add(self):
        self.client.force_authenticate(self.root)
        er = self._create_request_with_m2m()

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': er.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        new_episode = Episode.objects.filter(pk=response.data['id']).first()
        self.assertIsNotNone(
            new_episode,
            msg='New Episode should be created based on the submission'
        )
        self.assertEqual(
            set(map(lambda item: item['id'], er.episode_submission.characters.values('id'))),
            set(map(lambda item: item['id'], new_episode.characters.values('id'))),
            msg=f"Submission's characters set should match Episode's "
                f"after successful create"
        )

    def test_accept_edit(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_edit_01'].copy()
        data['current_episode'] = episode
        er = self._create_request_with_m2m(data)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': er.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f'Response should have OK status{response.data}'
        )
        er.refresh_from_db()
        episode.refresh_from_db()
        self.assertEqual(
            episode.name, er.episode_submission.name,
            msg='Episode\'s name should be updated based on the submission'
        )
        self.assertEqual(
            set(map(lambda item: item['id'], er.episode_submission.characters.values('id'))),
            set(map(lambda item: item['id'], episode.characters.values('id'))),
            msg=f"Submission's characters set should match Episode's "
                f"after successful create"
        )

    def test_accept_remove(self):
        self.client.force_authenticate(self.root)
        episode = self._create_episode_with_m2m()
        data = self.data['episode_request_remove_01'].copy()
        data['user'] = self.user
        data['current_episode'] = episode
        er = EpisodeRequest.objects.create(**data)

        data = self.data['accept_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['accept'], kwargs={'pk': er.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        removed_episode = Episode.objects.filter(pk=episode.pk).first()
        self.assertIsNone(
            removed_episode,
            msg='Episode should be removed'
        )
        self.assertIsNotNone(
            EpisodeRequest.objects.filter(pk=er.pk).first(),
            msg='Episode request should still exist after removing the Episode'
        )

    def test_reject(self):
        self.client.force_authenticate(self.root)
        er = self._create_request_with_m2m()

        data = self.data['reject_01'].copy()
        response = self.client.post(
            reverse(self.rev_urls['reject'], kwargs={'pk': er.pk}), data=data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Response should have OK status'
        )
        er.refresh_from_db()
        self.assertEqual(
            er.status, EpisodeRequest.STATUS_REJECTED,
            msg='Episode request should be rejected'
        )
        self.assertIsNotNone(
            er.requestlog_set.first(),
            msg='Episode request reject should be logged'
        )
        self.assertEqual(
            er.requestlog_set.first().moderator.pk, response.wsgi_request.user.pk,
            msg='Episode request reject log should be associated with '
                'the user who rejected it'
        )
