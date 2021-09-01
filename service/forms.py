from django import forms

from service.models import Service, ServiceCategory


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
