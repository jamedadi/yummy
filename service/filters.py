from django import forms

import django_filters

from service.models import Service


class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'class': 'form-control'}), lookup_expr='icontains'
    )

    service_type = django_filters.ChoiceFilter(
        choices=Service.SERVICE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
