from rest_framework.test import APITestCase

from movie_service.models import Title, TitleSubmission, Person, Character

from ... import init_users_and_groups
from .. import init_title_related_simple_objects


class AbstractApiModelTests(APITestCase):
    root, admin, moderator, user = None, None, None, None
    group_admin, group_moderator, group_user = None, None, None

    @classmethod
    def setUpTestData(cls):
        init_users_and_groups(cls)


class TitleTestsMixin(APITestCase):
    mixin_data = {
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
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        init_title_related_simple_objects()

    @classmethod
    def _get_title_data_no_m2m(cls, title_data):
        data_title = title_data.copy()
        no_m2m_keys = ['title', 'year', 'released', 'type', 'title_request']
        return {key: data_title[key] for key in no_m2m_keys if key in data_title}

    @classmethod
    def _create_title_with_m2m(cls, title_data=None, create_submission=False, tr=None):
        if title_data is None:
            title_data = cls.mixin_data['title_01']
        data = title_data.copy()
        if create_submission:
            create_class = TitleSubmission
            data['title_request'] = tr
        else:
            create_class = Title
        title_obj = create_class.objects.create(**cls._get_title_data_no_m2m(data))
        if data.get('languages') is not None:
            title_obj.languages.set(data['languages'])
        if data.get('countries') is not None:
            title_obj.countries.set(data['countries'])
        if data.get('genres') is not None:
            title_obj.genres.set(data['genres'])
        if data.get('characters') is not None:
            for character_d in data['characters']:
                character_d = character_d.copy()
                character_d['person'] = Person.objects.get(pk=character_d['person'])
                character = Character.objects.create(**character_d)
                title_obj.characters.add(character)
        if data.get('cast_members') is not None:
            for cast_member_d in data['cast_members']:
                p = Person.objects.get(pk=cast_member_d['person'])
                cast_member = title_obj.cast_members.create(person=p)
                cast_member.roles.set(cast_member_d['roles'])

        return title_obj
