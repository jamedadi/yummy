from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q

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

    def clean_username(self):
        if ServiceProvider.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError('There is a username!')
        return self.cleaned_data['username']

    def clean_email(self):
        if ServiceProvider.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('There is a email!')
        return self.cleaned_data['email']

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']

        if phone.startswith('98') and len(phone) == 12:
            if ServiceProvider.objects.filter(email=self.cleaned_data['phone_number']).exists():
                raise ValidationError('There is a phone_number!')
            else:
                return self.cleaned_data['phone_number']
        else:
            raise ValidationError('phone_number invalid!')

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('passwords not equal!')
        return self.cleaned_data['confirm_password']


class ServiceProviderLoginForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username, Email, Phone Number',
                'class': 'form-control'}
        )
    )

    password = forms.CharField(
        max_length=30,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'}
        )
    )

