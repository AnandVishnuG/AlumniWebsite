from django.core.exceptions import PermissionDenied

class CheckEditorGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = "Editor").exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CheckAdminGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = "Admin").exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied