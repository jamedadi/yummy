from django import forms

from address.models import Area
from service.models import Service, ServiceCategory, DeliveryArea, ServiceAvailableTime


class ServiceCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'service_type', 'minimum_purchase')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'minimum_purchase': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ServiceCategoryCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class DeliveryAreaCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = DeliveryArea
        fields = ('area',)
        widgets = {'area': forms.Select(attrs={'class': 'form-control'})}


class ServiceAvailableTimeCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceAvailableTime
        fields = ('day', 'open_time', 'close_time', 'is_close')
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'open_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'close_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_close': forms.NullBooleanSelect(attrs={'class': 'form-control'})
        }

