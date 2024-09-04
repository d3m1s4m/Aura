from rest_framework import permissions
from django.db.models import Q

from relations.models import FollowRelation, BlockRelation


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CanViewPostPermission(permissions.BasePermission):
    """
    check if the authenticated user can view the posts of a specific user.
    """
    def has_object_permission(self, request, view, obj):
        """
        return `True` if the user has permission to view the post, `False` otherwise.
        """
        user = request.user
        post_owner = obj.user

        # allow access to the post owner
        if user == post_owner:
            return True

        # deny access if either user has blocked the other
        if BlockRelation.objects.filter(
            Q(blocker=post_owner, blocked=user) |
            Q(blocker=user, blocked=post_owner)
        ).exists():
            return False

        # allow access if the post owner's profile is public
        if not post_owner.is_private:
            return True

        # allow access if the user follows the post owner and the follow request is accepted
        return FollowRelation.objects.filter(from_user=user, to_user=post_owner, is_accepted=True).exists()
