from django import template

register = template.Library()


@register.simple_tag()
def delivery_area_string(service):
    area_list = list()
    for delivery in service.delivery_areas.all():
        area_list.append(delivery.area.name)
    return ', '.join(area_list)
