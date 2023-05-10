from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

import six
def group_required(groups, login_url=None, raise_exception=False):
    if isinstance(groups, six.string_types):
        groups = (groups,)
    def check_perms(user):
        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)