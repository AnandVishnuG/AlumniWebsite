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

class CheckTreasurerGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = "Treasurer").exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
class CheckAdminOrTreasurerGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in = ("Admin","Treasurer")).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
class CheckAdminOrEditorGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in = ("Admin","Editor")).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
class CheckEditorOrTreasurerGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in = ("Editor","Treasurer")).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied