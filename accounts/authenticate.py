from django.contrib.auth.backends import BaseBackend

from accounts.models import Customer, ServiceProvider


class PhoneNumberPasswordBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            customer = Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            return None
        else:
            if password:  # if the password is sent via the form
                if customer.check_password(password):
                    return customer
                else:
                    return None
            return customer

    def get_user(self, user_id):
        try:
            customer = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
        else:
            return customer


class ServiceProviderAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = ServiceProvider.objects.get(username=username, password=password)
            return user

        except ServiceProvider.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ServiceProvider.objects.get(pk=user_id)
        except ServiceProvider.DoesNotExist:
            return None
