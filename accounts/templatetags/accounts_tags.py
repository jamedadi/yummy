from django import template
from django.contrib.auth import get_user_model

from accounts.models import Customer, ServiceProvider

User = get_user_model()

register = template.Library()


@register.simple_tag
def is_customer(user):
    if isinstance(user, Customer):
        return True
    return False


@register.simple_tag
def is_service_provider(user):
    if isinstance(user, ServiceProvider):
        return True
    return False


@register.simple_tag
def is_admin_user(user):
    if isinstance(user, User):
        return True
    return False
