from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from accounts.models import ServiceProvider


class ServiceProviderAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = ServiceProvider.objects.get(username=username, password=password)
            return user

        except ServiceProvider.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
