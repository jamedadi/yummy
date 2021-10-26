from abc import ABC

from accounts.utils import IsServiceProvider


class CustomServiceIsServiceProvider(ABC, IsServiceProvider):
    def test_func(self):
        result = super().test_func()
        obj = self.get_object()
        return obj.service_provider == self.request.user and result
