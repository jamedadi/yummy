from datetime import datetime, timedelta
from functools import wraps
from random import randint
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url


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


def user_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def check_is_not_authenticated(user):
    return not user.is_authenticated


def check_user_pk(user, **kwargs):
    return user.pk == kwargs['pk']
