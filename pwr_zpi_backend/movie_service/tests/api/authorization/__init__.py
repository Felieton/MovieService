from django.db import transaction

from rest_framework.test import APITestCase
from rest_framework import status

from ... import init_users_and_groups


class AbstractApiModelAuthTests(APITestCase):
    root, admin, moderator, user = None, None, None, None
    group_admin, group_moderator, group_user = None, None, None
    actions_tests = {
        'create': [],
        'delete': [],
        'update': [],
        'partial_update': [],
        'list': [],
        'retrieve': [],
    }

    @classmethod
    def setUpTestData(cls):
        init_users_and_groups(cls)

    def helper_test_general_access(self, data, helper_fun):
        for user, expected_status in data:
            with self.subTest(user=user, expected_status=expected_status), \
                    transaction.atomic():
                helper_fun(user, expected_status)
                # force rollback on innermost atomic block
                transaction.set_rollback(True)


class RequestPermissionsMixin(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actions_tests = {
            'create': [
                (cls.root, status.HTTP_201_CREATED),
                (cls.admin, status.HTTP_201_CREATED),
                (cls.moderator, status.HTTP_201_CREATED),
                (cls.user, status.HTTP_201_CREATED),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'delete': [
                (cls.root, status.HTTP_204_NO_CONTENT),
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
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'retrieve': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'accept': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ],
            'reject': [
                (cls.root, status.HTTP_200_OK),
                (cls.admin, status.HTTP_200_OK),
                (cls.moderator, status.HTTP_200_OK),
                (cls.user, status.HTTP_403_FORBIDDEN),
                (None, status.HTTP_401_UNAUTHORIZED),
            ]
        }
