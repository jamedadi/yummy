from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

User = get_user_model()


class ServiceProviderAuthentication(BaseBackend):
    def authenticate(self, request, username_email=None, password=None):
        try:
            user = User.objects.get(Q(username=username_email) | Q(email=username_email), password=password)
            return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
