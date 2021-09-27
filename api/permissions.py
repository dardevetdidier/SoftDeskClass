from rest_framework import permissions
from .models import Project, Contributor


class ProjectAuthorAllContributorCreateRead(permissions.BasePermission):
    """
    Projects Permissions.
    View level : Checks if user is authenticated.
    Object level : Author is allowed to Create, Read, Update, Delete.
                   Contributors are allowed to Create and Read.
    """
    edit_methods = ('PUT', 'DELETE')

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print(obj)
        print(request.user)
        print(obj.author_user_id)
        print(obj.contributors.all())

        if obj.author_user_id == request.user:
            return True

        if request.user in obj.contributors.all() and request.method not in self.edit_methods:
            return True

        return False


class IssueAuthorAllContributorCreateRead(permissions.BasePermission):
    edit_methods = ('PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print(obj.project_id.contributors.all())
        print(obj.author_user_id)

        if obj.author_user_id == request.user:
            return True

        if request.user in obj.project_id.contributors.all() and request.method not in self.edit_methods:
            return True

        return False


class CommentAuthorAllContributorCreateRead(permissions.BasePermission):
    edit_methods = ('PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print(obj.issue_id.project_id.contributors.all())
        print(obj.author_user_id)

        if obj.author_user_id == request.user:
            return True

        if request.user in obj.issue_id.project_id.contributors.all() and request.method not in self.edit_methods:
            return True

        return False

