import distutils.util
from typing import Tuple

from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.views.generic.base import RedirectView, View as DjangoView

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from dj_rest_auth.registration.views import SocialLoginView

import rest_framework.status
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ParseError

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, filters, mixins, views

from .scraper import getFilmInfoIMDB, getFilmInfoFilmweb, getBySearchIMDB, \
    getBySearchFilmweb, getPageSource, getFromPageSourceWithXPATH, \
    getListFromPageSourceWithXPATH

from ipware import get_client_ip

from . import serializers
from .models import User, CastRole, CastMember, Character, RequestLog, Person, \
    PersonRequest, Title, TitleRequest, Lang, Genre, Country, ActionLog, \
    Episode, EpisodeRequest, Review, Achievement, ScraperSites, AbstractRequest
from .permissions import DjangoModelPermissionsWithView
from . import permissions as perms

from urllib.parse import urlparse


# auth
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'https://movie-service-iota.vercel.app/login'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # identical to the one provided in the authorization request
    # more info: https://datatracker.ietf.org/doc/html/rfc6749#section-4.1.3
    callback_url = 'https://movie-service-iota.vercel.app/login'
    client_class = OAuth2Client


def check_param(q_param):
    return q_param is not None


def check_array_param(q_param):
    if q_param is not None:
        if q_param == '' \
                or not isinstance((q_param := q_param.split(',')), list) \
                or not all([item.isnumeric() for item in q_param]):
            raise ParseError(detail=f'Invalid array argument: \'{q_param}\'')
        return True
    return False


def filter_queryset(queryset: QuerySet, request,
                    q_filters: list[Tuple[str, str]], array_params=False):
    kw_filters = {}
    for q_param_name, filter_kw in q_filters:
        param = request.query_params.get(q_param_name)
        if array_params:
            if check_array_param(param):
                kw_filters[filter_kw] = param.split(',')
        elif check_param(param):
            kw_filters[filter_kw] = param

    res_qs = queryset.filter(**kw_filters)
    return res_qs.distinct() if array_params else res_qs


def filter_queryset_requests_closed(queryset: QuerySet, request):
    is_closed = request.query_params.get('isClosed')
    if is_closed is not None:
        try:
            is_closed = bool(distutils.util.strtobool(is_closed))
        except ValueError:
            raise ValidationError({'detail': 'Invalid param isClosed value provided'})
        if is_closed:
            res_qs = queryset.exclude(status=AbstractRequest.STATUS_PENDING)
        else:
            res_qs = queryset.filter(status=AbstractRequest.STATUS_PENDING)
    else:
        res_qs = queryset.filter()
    return res_qs


class CreateActionLogMixin:
    def _create_action_log(self, details, log_type, request=None, user=None):
        if request is None:
            request = self.request
        if user is not None:
            log_type = ActionLog.LOG_USER
        ip_address, _ = get_client_ip(request)
        log_data = {
            'moderator': request.user.pk,
            'ip_address': ip_address,
            'log_type': log_type,
            'details': details,
            'user': user.pk if user else None,
        }
        log_serializer = serializers.ActionLogSerializer(data=log_data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()


class CreateSimpleNameActionLog(CreateActionLogMixin):
    ACTION_LOG_TAG_PREFIX = 'OBJECT'
    ACTION_LOG_MODEL_NAME = 'object'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        admin: User = request.user
        self._create_action_log(
            f"[{self.ACTION_LOG_TAG_PREFIX}_CREATED] "
            f"Admin {admin.username} (#{admin.pk}) has created a new "
            f"{self.ACTION_LOG_MODEL_NAME} '{response.data['name']}' (#{response.data['id']})",
            ActionLog.LOG_ADMIN
        )
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        admin: User = request.user
        self._create_action_log(
            f"[{self.ACTION_LOG_TAG_PREFIX}_DELETED] "
            f"Admin {admin.username} (#{admin.pk}) has deleted an existing "
            f"{self.ACTION_LOG_MODEL_NAME} '{instance.name}' (#{instance.pk})",
            ActionLog.LOG_ADMIN
        )
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        admin: User = request.user
        self._create_action_log(
            f"[{self.ACTION_LOG_TAG_PREFIX}_UPDATED] "
            f"Admin {admin.username} (#{admin.pk}) has updated an existing "
            f"{self.ACTION_LOG_MODEL_NAME} '{instance.name}' (#{instance.pk})",
            ActionLog.LOG_ADMIN
        )
        return response


class UserViewSet(CreateActionLogMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    serializer_details_class = serializers.UserDetailsSerializer
    permission_classes = [perms.UserPermissions]
    filter_backends = [filters.OrderingFilter]

    def destroy(self, request, *args, **kwargs):
        instance: User = self.get_object()
        if instance.is_removed:
            raise Http404
        self.perform_destroy(instance)
        admin: User = request.user
        self._create_action_log(
            f"[USER_DELETED] "
            f"Admin {admin.username} (#{admin.pk}) has deleted an existing "
            f"user '{instance.username}' (#{instance.pk})",
            ActionLog.LOG_USER, user=instance
        )
        return Response(status=rest_framework.status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance: User):
        instance.is_removed = True
        instance.is_active = False
        instance.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        admin: User = request.user
        updated_items = ', '.join(request.data.keys())
        if admin.pk == instance.pk:
            self._create_action_log(
                f"User updated its {updated_items}",
                ActionLog.LOG_USER, user=instance
            )
        else:
            self._create_action_log(
                f"Admin {admin.username} (#{admin.pk}) has updated an existing "
                f"user's {updated_items}",
                ActionLog.LOG_USER, user=instance
            )
        return response

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class

        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('username', 'username__contains'),
            ('activeAfter', 'last_login__gt'),
            ('activeBefore', 'last_login__lt'),
            ('email', 'email__contains'),
        ]
        q_array_filters = [
            # get all users that have at least one of given groups
            ('groups', 'groups__in'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset

    @action(detail=True, methods=['post'])
    def restore(self, request, *args, **kwargs):
        user: User = self.get_object()
        # create log
        admin: User = request.user
        self._create_action_log(
            f"[USER_RESTORED] "
            f"Admin {admin.username} (#{admin.pk}) has restored an existing "
            f"user '{user.username}' (#{user.pk})",
            ActionLog.LOG_USER, user=user
        )
        # restore soft deleted user
        user.is_removed = False
        user.is_active = True
        user.save()

        return Response(status=rest_framework.status.HTTP_200_OK)


class CastRoleViewSet(CreateSimpleNameActionLog,
                      viewsets.ModelViewSet):
    queryset = CastRole.objects.all()
    serializer_class = serializers.CastRoleSerializer
    filter_backends = [filters.OrderingFilter]
    ACTION_LOG_TAG_PREFIX = 'CAST_ROLE'
    ACTION_LOG_MODEL_NAME = 'cast role'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class CastMemberViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = CastMember.objects.all()
    serializer_class = serializers.CastMemberDetailsSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('person', 'person'),
        ]
        q_array_filters = [
            ('roles', 'roles__in'),
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class CharacterViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Character.objects.all()
    serializer_class = serializers.CharacterDetailsSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
            ('person', 'person'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class RequestLogViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = serializers.RequestLogDetailsSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('titleRequest', 'title_request'),
            ('episodeRequest', 'episode_request'),
            ('personRequest', 'person_request'),
            ('moderator', 'moderator'),
            ('details', 'details__contains'),
            ('ip_address', 'ip_address__startswith'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)

        return queryset


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer
    serializer_detail_class = serializers.PersonDetailsSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
            ('surname', 'surname__contains'),
            ('birthdate', 'birthdate'),
            ('birthMonth', 'birthdate__month'),
            ('birthYear', 'birthdate__year'),
            ('details', 'details__contains'),
            ('country', 'country'),
        ]
        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class PersonRequestViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = PersonRequest.objects.all()
    serializer_class = serializers.PersonRequestSerializer
    serializer_details_class = serializers.PersonRequestDetailsSerializer
    permission_classes = [
        DjangoModelPermissionsWithView, perms.CanAcceptPersonRequest,
        perms.CanRejectPersonRequest
    ]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class
        elif self.action == 'list':
            return serializers.PersonRequestListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('action', 'action'),
            ('user', 'user'),
            ('header', 'header__contains'),
            ('description', 'description__contains'),
            ('currentPerson', 'current_person'),
            ('personSubmission', 'person_submission'),
            ('status', 'status'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset_requests_closed(queryset, self.request)

        return queryset

    def _log_action(self, person_request):
        request = self.request
        ip_address, _ = get_client_ip(request)
        log_data = {
            'details': request.data.get('details'),
            'person_request': person_request.pk,
            'moderator': request.user.pk,
            'ip_address': ip_address,
        }
        log_serializer = serializers.RequestLogSerializer(data=log_data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        response_data = None
        pr: PersonRequest = self.get_object()
        # create log
        self._log_action(pr)
        # add/edit/remove Person object
        if pr.action == PersonRequest.ACTION_ADD:
            person_serializer = serializers.PersonSerializer(data=pr.person_submission.as_dict())
            person_serializer.is_valid(raise_exception=True)
            person_serializer.save()
            response_data = person_serializer.data
        elif pr.action == PersonRequest.ACTION_EDIT:
            person_serializer = serializers.PersonSerializer(
                pr.current_person, data=pr.person_submission.as_dict()
            )
            person_serializer.is_valid(raise_exception=True)
            person_serializer.save()
            response_data = person_serializer.data
        elif pr.action == PersonRequest.ACTION_REMOVE:
            person = pr.current_person
            pr.current_person = None
            person.delete()
        else:
            raise ValidationError({
                'detail': 'Could not accept the request. '
                          'Request action property is invalid.'
            })
        # change status to accepted
        pr.status = PersonRequest.STATUS_ACCEPTED
        pr.save()

        return Response(response_data, status=rest_framework.status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        pr: PersonRequest = self.get_object()
        # create log
        self._log_action(pr)
        # change status to rejected
        pr.status = PersonRequest.STATUS_REJECTED
        pr.save()

        return Response(status=rest_framework.status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    serializer_details_class = serializers.TitleDetailsSerializer
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class

        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('title', 'title__icontains'),
            ('year', 'year'),
            ('plot', 'plot__contains'),
            ('type', 'type'),
            ('durationMin', 'duration__gt'),
            ('durationMax', 'duration__lt'),
            ('releasedAfter', 'released__gt'),
            ('releasedBefore', 'released__lt'),
            ('seasonsCount', 'seasons_count'),
            ('ratingMin', 'rating__gt'),
            ('ratingMax', 'rating__lt'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
            ('charactersPerson', 'characters__person'),
            ('castMembersPerson', 'cast_members__person'),
        ]
        q_array_filters = [
            ('characters', 'characters__in'),
            ('countries', 'countries__in'),
            ('genres', 'genres__in'),
            ('languages', 'languages__in'),
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class TitleRequestViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = TitleRequest.objects.all()
    serializer_class = serializers.TitleRequestSerializer
    serializer_details_class = serializers.TitleRequestDetailsSerializer
    permission_classes = [
        DjangoModelPermissionsWithView, perms.CanAcceptTitleRequest,
        perms.CanRejectTitleRequest
    ]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class
        elif self.action == 'list':
            return serializers.TitleRequestListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('action', 'action'),
            ('user', 'user'),
            ('header', 'header__contains'),
            ('description', 'description__contains'),
            ('status', 'status'),
            ('currentTitle', 'current_title'),
            ('titleSubmission', 'title_submission'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset_requests_closed(queryset, self.request)

        return queryset

    def _log_action(self, title_request):
        request = self.request
        ip_address, _ = get_client_ip(request)
        log_data = {
            'details': request.data.get('details'),
            'title_request': title_request.pk,
            'moderator': request.user.pk,
            'ip_address': ip_address,
        }
        log_serializer = serializers.RequestLogSerializer(data=log_data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        response_data = None
        tr: TitleRequest = self.get_object()
        # create log
        self._log_action(tr)
        # add/edit/remove Title object
        if tr.action == TitleRequest.ACTION_ADD:
            title_serializer = serializers.TitleSerializer(data=tr.title_submission.as_dict())
            title_serializer.is_valid(raise_exception=True)
            title_serializer.save()
            response_data = title_serializer.data
        elif tr.action == TitleRequest.ACTION_EDIT:
            title_serializer = serializers.TitleSerializer(
                tr.current_title, data=tr.title_submission.as_dict()
            )
            title_serializer.is_valid(raise_exception=True)
            title_serializer.save()
            response_data = title_serializer.data
        elif tr.action == TitleRequest.ACTION_REMOVE:
            title = tr.current_title
            tr.current_title = None
            title.delete()
        else:
            raise ValidationError({
                'detail': 'Could not accept the request. '
                          'Request action property is invalid.'
            })
        # change status to accepted
        tr.status = TitleRequest.STATUS_ACCEPTED
        tr.save()

        return Response(response_data, status=rest_framework.status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        tr: TitleRequest = self.get_object()
        # create log
        self._log_action(tr)
        # change status to rejected
        tr.status = TitleRequest.STATUS_REJECTED
        tr.save()

        return Response(status=rest_framework.status.HTTP_200_OK)


class LangViewSet(CreateSimpleNameActionLog,
                  viewsets.ModelViewSet):
    queryset = Lang.objects.all()
    serializer_class = serializers.LangSerializer
    filter_backends = [filters.OrderingFilter]
    ACTION_LOG_TAG_PREFIX = 'LANG'
    ACTION_LOG_MODEL_NAME = 'language'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class GenreViewSet(CreateSimpleNameActionLog,
                   viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = [filters.OrderingFilter]
    ACTION_LOG_TAG_PREFIX = 'GENRE'
    ACTION_LOG_MODEL_NAME = 'genre'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class CountryViewSet(CreateActionLogMixin,
                     viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    filter_backends = [filters.OrderingFilter]
    ACTION_LOG_TAG_PREFIX = 'COUNTRY'
    ACTION_LOG_MODEL_NAME = 'country'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
            ('shortName', 'short_name'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class ActionLogViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = ActionLog.objects.all()
    serializer_class = serializers.ActionLogDetailsSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('moderator', 'moderator'),
            ('logType', 'log_type'),
            ('details', 'details__contains'),
            ('ipAddress', 'ip_address__contains'),
            ('user', 'user'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)

        return queryset


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = serializers.EpisodeSerializer
    serializer_details_class = serializers.EpisodeDetailsSerializer
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class

        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
            ('plot', 'plot_contains'),
            ('releasedAfter', 'released__gt'),
            ('releasedBefore', 'released__lt'),
            ('season', 'season'),
            ('number', 'number'),
            ('durationMin', 'duration__gt'),
            ('durationMax', 'duration__lt'),
            ('title', 'title'),
            ('ratingMin', 'rating__gt'),
            ('ratingMax', 'rating__lt'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]
        q_array_filters = [
            ('characters', 'characters__in'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class EpisodeRequestViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = EpisodeRequest.objects.all()
    serializer_class = serializers.EpisodeRequestSerializer
    serializer_details_class = serializers.EpisodeRequestDetailsSerializer
    permission_classes = [
        DjangoModelPermissionsWithView, perms.CanAcceptEpisodeRequest,
        perms.CanRejectEpisodeRequest
    ]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_details_class
        elif self.action == 'list':
            return serializers.EpisodeRequestListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('action', 'action'),
            ('user', 'user'),
            ('header', 'header__contains'),
            ('description', 'description__contains'),
            ('currentEpisode', 'current_episode'),
            ('episodeSubmission', 'episode_submission'),
            ('status', 'status'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset_requests_closed(queryset, self.request)

        return queryset

    def _log_action(self, episode_request):
        request = self.request
        ip_address, _ = get_client_ip(request)
        log_data = {
            'details': request.data.get('details'),
            'episode_request': episode_request.pk,
            'moderator': request.user.pk,
            'ip_address': ip_address,
        }
        log_serializer = serializers.RequestLogSerializer(data=log_data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        response_data = None
        er: EpisodeRequest = self.get_object()
        # create log
        self._log_action(er)
        # add/edit/remove Episode object
        if er.action == EpisodeRequest.ACTION_ADD:
            episode_serializer = serializers.EpisodeSerializer(data=er.episode_submission.as_dict())
            episode_serializer.is_valid(raise_exception=True)
            episode_serializer.save()
            response_data = episode_serializer.data
        elif er.action == EpisodeRequest.ACTION_EDIT:
            episode_serializer = serializers.EpisodeSerializer(
                er.current_episode, data=er.episode_submission.as_dict()
            )
            episode_serializer.is_valid(raise_exception=True)
            episode_serializer.save()
            response_data = episode_serializer.data
        elif er.action == EpisodeRequest.ACTION_REMOVE:
            episode = er.current_episode
            er.current_episode = None
            episode.delete()
        else:
            raise ValidationError({
                'detail': 'Could not accept the request. '
                          'Request action property is invalid.'
            })
        # change status to accepted
        er.status = EpisodeRequest.STATUS_ACCEPTED
        er.save()

        return Response(response_data, status=rest_framework.status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        er: EpisodeRequest = self.get_object()
        # create log
        self._log_action(er)
        # change status to rejected
        er.status = EpisodeRequest.STATUS_REJECTED
        er.save()

        return Response(status=rest_framework.status.HTTP_200_OK)


class ReviewViewSet(CreateActionLogMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    serializer_details_class = serializers.ReviewDetailsSerializer
    permission_classes = [
        perms.ReviewPermissions,
        perms.CanAcceptReview, perms.CanRejectReview
    ]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return self.serializer_details_class

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance: Review = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        moderator: User = request.user
        reviewed = instance.title if instance.title is not None else instance.episode
        if moderator.pk == instance.user.pk:
            self._create_action_log(
                f"[REVIEW_DELETED] "
                f"User {instance.user.username} (#{instance.user.pk}) has deleted"
                f" his review: '{instance.header}' (#{instance.pk})"
                f" regarding reviewed (#{reviewed.pk})",
                ActionLog.LOG_USER, user=instance.user
            )
        else:
            self._create_action_log(
                f"[REVIEW_DELETED] "
                f"Moderator {moderator.username} (#{moderator.pk}) has deleted"
                f" an existing review: '{instance.header}' (#{instance.pk})"
                f" submitted by user {instance.user.username} (#{instance.user.pk})"
                f" regarding reviewed (#{reviewed.pk})",
                ActionLog.LOG_MODERATOR
            )

        if instance.episode is None:
            instance.title.update_avg_rating()
        else:
            instance.episode.update_avg_rating()

        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('user', 'user'),
            ('title', 'title'),
            ('titleIsNull', 'title__isnull'),
            ('episode', 'episode'),
            ('header', 'header__contains'),
            ('body', 'body__contains'),
            ('isAccepted', 'is_accepted'),
            ('ratingMin', 'rating__gt'),
            ('ratingMax', 'rating__lt'),
            ('createdAfter', 'created__gt'),
            ('createdBefore', 'created__lt'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        review: Review = self.get_object()
        if review.is_accepted:
            raise ValidationError({'detail': 'This review has been already accepted.'})
        moderator: User = request.user
        reviewed = review.title if review.title is not None else review.episode
        self._create_action_log(
            f"[REVIEW_ACCEPTED] "
            f"Moderator {moderator.username} (#{moderator.pk}) has accepted"
            f" the following review: '{review.header}' (#{review.pk})"
            f" submitted by user {review.user.username} (#{review.user.pk})"
            f" regarding reviewed (#{reviewed.pk})",
            ActionLog.LOG_MODERATOR
        )
        # change status to accepted
        review.is_accepted = True
        review.save()

        if review.episode is None:
            review.title.update_avg_rating()
        else:
            review.episode.update_avg_rating()

        return Response(status=rest_framework.status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        review: Review = self.get_object()
        if review.is_accepted:
            raise ValidationError({'detail': 'This review has been already accepted.'})
        moderator: User = request.user
        reviewed = review.title if review.title is not None else review.episode
        self._create_action_log(
            f"[REVIEW_REJECTED] "
            f"Moderator {moderator.username} (#{moderator.pk}) has rejected"
            f" the following review: '{review.header}' (#{review.pk})"
            f" submitted by user {review.user.username} (#{review.user.pk})"
            f" regarding reviewed (#{reviewed.pk})",
            ActionLog.LOG_MODERATOR
        )
        # remove rejected review
        review.delete()

        return Response(status=rest_framework.status.HTTP_200_OK)


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)

        return queryset


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = serializers.AchievementSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('name', 'name__contains'),
        ]

        q_array_filters = [
            ('ids', 'id__in')
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)
        queryset = filter_queryset(queryset, self.request, q_array_filters, array_params=True)

        return queryset


class ScraperSitesViewSet(viewsets.ModelViewSet):
    queryset = ScraperSites.objects.all()
    serializer_class = serializers.ScraperSitesSerializer
    permission_classes = [AllowAny]
    page_size_query_param = 'perPage'
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'list':
            return queryset

        q_filters = [
            ('netloc', 'netloc__contains'),
            ('title', 'title__contains'),
            ('director', 'director__contains'),
            ('genres', 'genres__contains'),
            ('split_genre_by', 'split_genre_by__contains'),
            ('countries', 'countries__contains'),
            ('split_countries_by', 'split_countries_by__contains'),
            ('year', 'year__contains'),
            ('release_date', 'release_date__contains'),
        ]

        queryset = filter_queryset(queryset, self.request, q_filters)

        return queryset


class ScraperAPIView(views.APIView):
    serializer_class = serializers.ScraperSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        print(request)
        scrapeUrl = request.data["url"]
        film_info = {}
        if request.data["site"] == 'imdb':
            if request.data["mode"] == 'url':
                film_info = getFilmInfoIMDB(scrapeUrl)
            elif request.data["mode"] == 'title':
                return HttpResponse(status=500)
                film_info = getFilmInfoIMDB(getBySearchIMDB(scrapeUrl))
        elif request.data['site'] == 'filmweb':
            if request.data["mode"] == 'url':
                film_info = getFilmInfoFilmweb(scrapeUrl)
            elif request.data["mode"] == 'title':
                return HttpResponse(status=500)
                film_info = getFilmInfoFilmweb(getBySearchFilmweb(scrapeUrl))
        elif request.data["site"] == 'other':
            if request.data["mode"] == 'title':
                return HttpResponse(status=500)
            elif request.data["mode"] == 'url':
                scraper_site = ScraperSites.objects.get(netloc=urlparse(request.data["url"]).netloc)
                if scraper_site is None:
                    return HttpResponse(status=500)
                else:
                    page_source = getPageSource(request.data["url"])

                    title = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.title)
                    director = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.director)
                    genres = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.genres)
                    countries = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.countries)
                    year = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.year)
                    release_date = getFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.release_date)
                    duration = getListFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.duration)
                    plot = getListFromPageSourceWithXPATH(page_source=page_source, xpath=scraper_site.duration)

                    film_info["title"] = title
                    film_info["director"] = director
                    film_info["genres"] = genres
                    film_info["countries"] = countries
                    film_info["year"] = year
                    film_info["release_date"] = release_date
                    film_info["duration"] = duration
                    film_info["plot"] = plot
        return Response(film_info)


class RegistrationRedirectView(RedirectView):
    permanent = True
    url = "https://movie-service-iota.vercel.app/verification/%(key)s"


class ReverseMatchNullView(DjangoView):
    def dispatch(self, request, *args, **kwargs):
        raise Http404
