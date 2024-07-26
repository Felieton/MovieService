from django.contrib.auth.models import Group

from movie_service.models import User


def init_groups(cls):
    cls.group_admin = Group.objects.get(name='Administrator')
    cls.group_moderator = Group.objects.get(name='Moderator')
    cls.group_user = Group.objects.get(name='User')


def init_users(cls):
    cls.root = User.objects.create_superuser('root', 'root@example.com', '1234')

    cls.admin = User.objects.create_user('admin', 'admin@example.com', '1234')
    cls.admin.groups.add(cls.group_admin)

    cls.moderator = User.objects.create_user('moderator', 'moderator@example.com', '1234')
    cls.moderator.groups.add(cls.group_moderator)

    cls.user = User.objects.create_user('user', 'user@example.com', '1234')
    cls.user.groups.add(cls.group_user)


def init_users_and_groups(cls):
    init_groups(cls)
    init_users(cls)
