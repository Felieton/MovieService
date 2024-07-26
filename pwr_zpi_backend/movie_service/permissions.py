import copy
from rest_framework.permissions import DjangoModelPermissions, BasePermission, \
    DjangoModelPermissionsOrAnonReadOnly


class DjangoModelPermissionsWithView(DjangoModelPermissions):

    def __init__(self):
        super().__init__()
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class UserPermissions(DjangoModelPermissionsOrAnonReadOnly):
    """
    Permission allowing user to self edit fields that
    are in SELF_UPDATE_FIELDS array
    """
    SELF_UPDATE_FIELDS = ['photo', 'settings', 'watchlist', 'description']

    def has_permission(self, request, view):
        if request.method != 'PATCH':
            return super().has_permission(request, view)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'PATCH':
            return True
        if not request.user or not request.user.is_authenticated or \
                request.user.pk != obj.pk:
            return super().has_permission(request, view)

        data: dict = request.data
        for field in data.keys():
            if field not in self.SELF_UPDATE_FIELDS:
                return super().has_permission(request, view)

        return True


class ReviewPermissions(DjangoModelPermissionsOrAnonReadOnly):
    """
    Permission allowing owner of the review to delete it
    """

    def has_permission(self, request, view):
        if request.method != 'DELETE':
            return super().has_permission(request, view)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        if not request.user or not request.user.is_authenticated or \
                request.user.pk != obj.user_id:
            return super().has_permission(request, view)

        return True


class CanAcceptPersonRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'accept':
            return True
        return request.user.has_perm('movie_service.accept_personrequest')


class CanRejectPersonRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'reject':
            return True
        return request.user.has_perm('movie_service.reject_personrequest')


class CanAcceptTitleRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'accept':
            return True
        return request.user.has_perm('movie_service.accept_titlerequest')


class CanRejectTitleRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'reject':
            return True
        return request.user.has_perm('movie_service.reject_titlerequest')


class CanAcceptEpisodeRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'accept':
            return True
        return request.user.has_perm('movie_service.accept_episoderequest')


class CanRejectEpisodeRequest(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'reject':
            return True
        return request.user.has_perm('movie_service.reject_episoderequest')


class CanAcceptReview(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'accept':
            return True
        return request.user.has_perm('movie_service.accept_review')


class CanRejectReview(BasePermission):

    def has_permission(self, request, view):
        if view.action != 'reject':
            return True
        return request.user.has_perm('movie_service.reject_review')
