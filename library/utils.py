from abc import ABC

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


class CustomUserPasses(ABC, UserPassesTestMixin):
    raise_exception = True

    def handle_no_permission(self, path_url=None, redirect=False):
        if redirect:
            return HttpResponseRedirect(path_url)

        else:
            raise PermissionDenied(self.get_permission_denied_message())

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()

        if isinstance(self.test_func(), tuple):
            user_test_bool, redirect, path_url = user_test_result
            if not user_test_bool:
                return self.handle_no_permission(path_url, redirect)

        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
