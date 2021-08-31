from django import template

from accounts.models import Customer, ServiceProvider

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
