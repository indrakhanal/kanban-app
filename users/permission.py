from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.contrib.auth.models import User
from core.models import KanBanBoard

class IsAdminUser(permissions.BasePermission):
	message = 'Permission Denied for current user'
	def has_permission(self, request, view):
		user = get_object_or_404(User, id = request.user.id)
		if user.is_active and user.is_staff:
			return True
		return False


class IsBoardOwner(permissions.BasePermission):
    message = "You are not allowed to do current action"
    def has_permission(self, request, view):
        user = get_object_or_404(KanBanBoard, id=request.user.id)
        if user:
            if user.user.id:
                return True
        else:
            return False