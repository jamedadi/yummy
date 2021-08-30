from datetime import datetime, timedelta
from random import randint

from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import Customer, ServiceProvider


def check_expire_time(request):
    try:
        expire_time = datetime.strptime(request.session['created-time'], '%Y-%m-%d %H:%M:%S')
    except KeyError:
        expire_time = None

    if expire_time:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if (now - expire_time) > timedelta(minutes=2):
            del request.session['code']
            del request.session['created-time']


def set_phone_number_session(request, phone_number):
    request.session['phone_number'] = phone_number
    request.session['code'] = randint(1000, 9999)
    request.session['created_time'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(request.session['code'])
    print(request.session['created_time'])


def check_is_not_authenticated(user):
    return not user.is_authenticated


def can_set_password(user):
    return not user.password


class IsCustomer(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return isinstance(self.request.user, Customer)


class IsServiceProvider(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return isinstance(self.request.user, ServiceProvider)


class CheckCustomerAccessPk(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return isinstance(user, Customer) and user.pk == self.kwargs['pk']


class CheckServiceProviderAccessPk(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return isinstance(user, ServiceProvider) and user.pk == self.kwargs['pk']
