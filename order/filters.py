from django import forms

import django_filters

from order.models import Order


class OrderFilter(django_filters.FilterSet):
    created_time = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'data-date-format': 'YYYY-MMMM-DD '}),
        lookup_expr='contains'
    )

    status = django_filters.ChoiceFilter(
        choices=Order.STATUS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )