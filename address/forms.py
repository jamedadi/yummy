from django import forms

from address.models import CustomerAddress, ServiceAddress

base_fields = ('state', 'city', 'area', 'street', 'alley', 'floor', 'plaque')
base_widgets = {
    'state': forms.Select(attrs={'class': 'form-control'}),
    'city': forms.Select(attrs={'class': 'form-control'}),
    'area': forms.Select(attrs={'class': 'form-control'}),
    'street': forms.TextInput(attrs={'class': 'form-control'}),
    'alley': forms.TextInput(attrs={'class': 'form-control'}),
    'floor': forms.NumberInput(attrs={'class': 'form-control'}),
    'plaque': forms.NumberInput(attrs={'class': 'form-control'}),
}


class CustomerAddressCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = base_fields
        widgets = base_widgets


class ServiceAddressCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceAddress
        fields = base_fields
        widgets = base_widgets
