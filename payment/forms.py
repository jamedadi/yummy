from django import forms

from address.models import CustomerAddress
from gateway.models import Gateway


class AddressSelectForm(forms.Form):
    address = forms.ModelChoiceField(queryset=CustomerAddress.objects.all(), widget=forms.RadioSelect)


class GatewaySelectForm(forms.Form):
    gateway = forms.ModelChoiceField(queryset=Gateway.objects.filter(is_enable=True), widget=forms.RadioSelect)
