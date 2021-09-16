from django import template

register = template.Library()


@register.simple_tag
def filter_category(queryset, category):
    return queryset.filter(category=category)
