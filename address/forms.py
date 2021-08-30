from django import forms

from address.models import CustomerAddress


class CustomerAddressCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ('state', 'city', 'area', 'street', 'alley', 'floor', 'plaque')
        widgets = {
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'alley': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'plaque': forms.NumberInput(attrs={'class': 'form-control'}),
        }
