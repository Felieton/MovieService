from django.contrib.auth.models import Group

from .models import User, CastRole, CastMember, Character, RequestLog, \
    Person, PersonSubmission, PersonRequest, Title, TitleSubmission, \
    TitleRequest, Lang, Genre, Country, ActionLog, Episode, \
    EpisodeSubmission, EpisodeRequest, Review, UserSettings, Achievement, ScraperSites
from rest_framework import serializers

from drf_writable_nested import mixins as wr_mixins


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        read_only_fields = fields


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'id', 'email_visible', 'watchlist_visible', 'achievements_visible'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'name'
        ]


class UserSerializer(wr_mixins.NestedUpdateMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_active', 'is_removed',
            'date_joined', 'last_login', 'groups', 'settings', 'achievements',
            'watchlist', 'description', 'photo'
        ]
        read_only_fields = [
            'is_active', 'is_removed', 'date_joined', 'last_login'
        ]
        extra_kwargs = {
            'settings': {'write_only': True},
            'achievements': {'write_only': True},
            'description': {'write_only': True},
            'watchlist': {'write_only': True},
            'photo': {'allow_null': True},
        }

    settings = UserSettingsSerializer(required=False, write_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        current_user = self.context['request'].user
        if instance.pk == current_user.pk or \
                current_user.has_perm('movie_service.change_user'):
            return ret

        if not instance.settings.email_visible:
            del ret['email']

        return ret


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        '''
        All user fields are as follows:
        fields = [
            'id', 'username', 'email', 'is_staff', 'is_active', 'is_removed',
            'date_joined', 'last_login', 'is_superuser', 'groups',
            'user_permissions', 'settings', 'achievements', 'watchlist'
        ]
        '''
        fields = [
            'id', 'username', 'email', 'is_active', 'is_removed',
            'date_joined', 'last_login', 'groups', 'settings', 'achievements',
            'watchlist', 'description', 'photo'
        ]
        read_only_fields = fields

    groups = GroupSerializer(many=True, read_only=True)
    settings = UserSettingsSerializer(read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        current_user = self.context['request'].user
        if instance.pk == current_user.pk or \
                current_user.has_perm('movie_service.change_user'):
            return ret

        if not instance.settings.email_visible:
            del ret['email']
        if not instance.settings.watchlist_visible:
            del ret['watchlist']
        if not instance.settings.achievements_visible:
            del ret['achievements']

        return ret


class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lang
        fields = [
            'id', 'name'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id', 'name'
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'short_name'
        ]


class CastRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastRole
        fields = [
            'id', 'name'
        ]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id', 'name', 'surname', 'birthdate', 'country', 'details', 'photo'
        ]
        extra_kwargs = {
            'country': {'write_only': True},
            'photo': {'allow_null': True},
        }


class PersonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id', 'name', 'surname', 'birthdate', 'country', 'details', 'photo'
        ]
        read_only_fields = fields

    country = CountrySerializer(read_only=True)


class PersonSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonSubmission
        fields = [
            'id', 'name', 'surname', 'birthdate', 'country', 'details', 'photo'
        ]
        extra_kwargs = {
            'birthdate': {'write_only': True},
            'country': {'write_only': True},
            'details': {'write_only': True},
            'photo': {'allow_null': True},
        }


class PersonSubmissionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonSubmission
        fields = [
            'id', 'name', 'surname', 'birthdate', 'country', 'details', 'photo'
        ]
        read_only_fields = fields

    country = CountrySerializer(read_only=True)


class PersonRequestSerializer(wr_mixins.NestedCreateMixin,
                              serializers.ModelSerializer):
    class Meta:
        model = PersonRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_person', 'person_submission', 'status', 'created',
        ]
        read_only_fields = [
            'status', 'created'
        ]
        extra_kwargs = {
            'description': {'write_only': True},
            'current_person': {'write_only': True},
        }

    person_submission = PersonSubmissionSerializer(required=False, write_only=True)
    # it's being set in the view just before creating
    # = user requesting create
    user = UserSerializer(read_only=True)

    def validate(self, data):
        def check_required(data_key):
            if data.get(data_key) is None:
                raise serializers.ValidationError({data_key: 'This field is required.'})

        def check_blank(data_key):
            if data.get(data_key) is not None:
                raise serializers.ValidationError({data_key: 'This field must be blank.'})

        req_action = data.get('action')
        if req_action == PersonRequest.ACTION_ADD:
            check_required('person_submission')
            check_blank('current_person')
        elif req_action == PersonRequest.ACTION_EDIT:
            check_required('person_submission')
            check_required('current_person')
        elif req_action == PersonRequest.ACTION_REMOVE:
            check_required('current_person')
            check_blank('person_submission')
        return data


class PersonRequestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_person', 'person_submission', 'status', 'created'
        ]
        read_only_fields = fields

    user = UserSerializer(read_only=True)
    current_person = PersonDetailsSerializer(read_only=True)
    person_submission = PersonSubmissionDetailsSerializer(read_only=True)


class PersonRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_person', 'status', 'created'
        ]
        read_only_fields = fields

    user = UserSerializer(read_only=True)
    current_person = PersonSerializer(read_only=True)


class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = [
            'id', 'person', 'roles'
        ]


class CastMemberDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = [
            'id', 'person', 'roles'
        ]

    person = PersonSerializer(read_only=True)
    roles = CastRoleSerializer(many=True, read_only=True)


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            'id', 'name', 'person'
        ]


class CharacterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            'id', 'name', 'person'
        ]
        read_only_fields = fields

    person = PersonSerializer(read_only=True)


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            'id', 'title', 'year', 'plot', 'created', 'released', 'type',
            'seasons_count', 'duration', 'rating', 'languages', 'countries',
            'genres', 'characters', 'cast_members', 'poster'
        ]
        read_only_fields = [
            'created', 'rating'
        ]
        extra_kwargs = {
            'languages': {'write_only': True},
            'countries': {'write_only': True},
            'genres': {'write_only': True},
            'characters': {'write_only': True},
            'cast_members': {'write_only': True},
            'poster': {'allow_null': True},
        }


class TitleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            'id', 'title', 'year', 'plot', 'created', 'released', 'type',
            'seasons_count', 'duration', 'rating', 'languages', 'countries',
            'genres', 'characters', 'cast_members', 'poster'
        ]
        read_only_fields = fields


class TitleSubmissionSerializer(wr_mixins.NestedCreateMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = TitleSubmission
        fields = [
            'id', 'title', 'year', 'plot', 'created', 'released', 'type',
            'seasons_count', 'duration', 'languages', 'countries', 'genres',
            'characters', 'cast_members', 'poster'
        ]
        read_only_fields = [
            'created'
        ]
        extra_kwargs = {
            'languages': {'write_only': True},
            'countries': {'write_only': True},
            'genres': {'write_only': True},
            'poster': {'allow_null': True},
        }

    characters = CharacterSerializer(many=True, required=False, write_only=True)
    cast_members = CastMemberSerializer(many=True, required=False, write_only=True)


class TitleSubmissionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleSubmission
        fields = [
            'id', 'title', 'year', 'plot', 'created', 'released', 'type',
            'seasons_count', 'duration', 'languages', 'countries', 'genres',
            'characters', 'cast_members', 'poster'
        ]
        read_only_fields = fields

    languages = LangSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    characters = CharacterDetailsSerializer(many=True, read_only=True)
    cast_members = CastMemberDetailsSerializer(many=True, read_only=True)


class TitleRequestSerializer(wr_mixins.NestedCreateMixin,
                             serializers.ModelSerializer):
    class Meta:
        model = TitleRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_title', 'title_submission', 'status', 'created',
        ]
        read_only_fields = [
            'status', 'created'
        ]
        extra_kwargs = {
            'description': {'write_only': True},
            'current_title': {'write_only': True},
        }

    title_submission = TitleSubmissionSerializer(required=False, write_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, data):
        def check_required(data_key):
            if data.get(data_key) is None:
                raise serializers.ValidationError({data_key: 'This field is required.'})

        def check_blank(data_key):
            if data.get(data_key) is not None:
                raise serializers.ValidationError({data_key: 'This field must be blank.'})

        req_action = data.get('action')
        if req_action == TitleRequest.ACTION_ADD:
            check_required('title_submission')
            check_blank('current_title')
        elif req_action == TitleRequest.ACTION_EDIT:
            check_required('title_submission')
            check_required('current_title')
        elif req_action == TitleRequest.ACTION_REMOVE:
            check_required('current_title')
            check_blank('title_submission')
        return data


class TitleRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_title', 'status', 'created',
        ]
        read_only_fields = fields

    current_title = TitleSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class TitleRequestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_title', 'title_submission', 'status', 'created',
        ]
        read_only_fields = fields

    current_title = TitleDetailsSerializer(read_only=True)
    title_submission = TitleSubmissionDetailsSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'id', 'name', 'plot', 'released', 'created', 'season', 'number',
            'duration', 'title', 'characters', 'rating'
        ]
        read_only_fields = [
            'created', 'rating'
        ]
        extra_kwargs = {
            'characters': {'write_only': True},
        }


class EpisodeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'id', 'name', 'plot', 'released', 'created', 'season', 'number',
            'duration', 'title', 'characters', 'rating'
        ]
        read_only_fields = fields

    title = TitleDetailsSerializer(read_only=True)


class EpisodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeSubmission
        fields = [
            'id', 'name', 'plot', 'released', 'created', 'season', 'number',
            'duration', 'title', 'characters'
        ]
        read_only_fields = [
            'created'
        ]
        extra_kwargs = {
            'characters': {'write_only': True},
        }


class EpisodeSubmissionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeSubmission
        fields = [
            'id', 'name', 'plot', 'released', 'created', 'season', 'number',
            'duration', 'title', 'characters'
        ]
        read_only_fields = fields

    title = TitleDetailsSerializer(read_only=True)
    characters = CharacterDetailsSerializer(many=True, read_only=True)


class EpisodeRequestSerializer(wr_mixins.NestedCreateMixin,
                               serializers.ModelSerializer):
    class Meta:
        model = EpisodeRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_episode', 'episode_submission', 'status', 'created',
        ]
        read_only_fields = [
            'status', 'created'
        ]
        extra_kwargs = {
            'description': {'write_only': True},
            'current_episode': {'write_only': True},
        }

    episode_submission = EpisodeSubmissionSerializer(required=False, write_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, data):
        def check_required(data_key):
            if data.get(data_key) is None:
                raise serializers.ValidationError({data_key: 'This field is required.'})

        def check_blank(data_key):
            if data.get(data_key) is not None:
                raise serializers.ValidationError({data_key: 'This field must be blank.'})

        req_action = data.get('action')
        if req_action == EpisodeRequest.ACTION_ADD:
            check_required('episode_submission')
            check_blank('current_episode')
        elif req_action == EpisodeRequest.ACTION_EDIT:
            check_required('episode_submission')
            check_required('current_episode')
        elif req_action == EpisodeRequest.ACTION_REMOVE:
            check_required('current_episode')
            check_blank('episode_submission')
        return data


class EpisodeRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_episode', 'status', 'created',
        ]
        read_only_fields = fields

    current_episode = EpisodeSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class EpisodeRequestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeRequest
        fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_episode', 'episode_submission', 'status', 'created',
        ]
        read_only_fields = fields

    current_episode = EpisodeDetailsSerializer(read_only=True)
    episode_submission = EpisodeSubmissionDetailsSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = [
            'id', 'title_request', 'episode_request', 'person_request',
            'details', 'moderator', 'ip_address', 'created'
        ]
        read_only_fields = [
            'created'
        ]

    def validate(self, data):
        def check_blank(data_key):
            if data.get(data_key) is not None:
                raise serializers.ValidationError({data_key: 'This field must be blank.'})

        if data.get('title_request') is not None:
            check_blank('episode_request')
            check_blank('person_request')
        elif data.get('episode_request') is not None:
            check_blank('person_request')
        elif data.get('person_request') is None:
            raise serializers.ValidationError({
                'detail': 'One of the following fields is required: '
                          'title_request, episode_request, person_request'
            })
        return data


class RequestLogDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = [
            'id', 'title_request', 'episode_request', 'person_request',
            'details', 'moderator', 'ip_address', 'created'
        ]
        read_only_fields = fields

    moderator = UserSerializer(read_only=True)


class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = [
            'id', 'details', 'moderator', 'ip_address', 'created', 'user',
            'log_type'
        ]
        read_only_fields = [
            'created'
        ]


class ActionLogDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = [
            'id', 'details', 'moderator', 'ip_address', 'created', 'user',
            'log_type'
        ]
        read_only_fields = fields

    moderator = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'title', 'episode', 'header', 'body', 'rating',
            'is_accepted', 'created'
        ]
        read_only_fields = [
            'user', 'is_accepted', 'created'
        ]

    user = UserSerializer(read_only=True)


class ReviewDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'title', 'episode', 'header', 'body', 'rating',
            'is_accepted', 'created'
        ]
        read_only_fields = fields

    user = UserSerializer(read_only=True)
    title = TitleSerializer(read_only=True)
    episode = EpisodeSerializer(read_only=True)


class ScraperSerializer(serializers.Serializer):
    pass


class ScraperSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScraperSites
        fields = [
            'id', 'netloc', 'title', 'director', 'genres', 'countries',
            'year', 'release_date', 'plot'
        ]
