from django import forms
from django.core.exceptions import ValidationError

from accounts.models import ServiceProvider


class ServiceProviderRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control'}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control'}
        )
    )

    class Meta:
        model = ServiceProvider
        fields = ('username', 'email', 'phone_number', 'password', 'confirm_password')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

