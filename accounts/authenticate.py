from django.contrib.auth.backends import BaseBackend
from accounts.models import Customer


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
            return customer
