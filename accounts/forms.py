from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _

from accounts.models import ServiceProvider, Customer
from accounts.utils import phone_number_validator


class CustomerLoginRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=12,
                                   validators=[
                                       int_list_validator(message=_('only digits are accepted')),
                                       phone_number_validator
                                   ],
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'phone number'})
                                   )


class CustomerCodeConfirmForm(forms.Form):
    code = forms.CharField(
        validators=[int_list_validator(message=_('only digits are accepted'))],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('confirmation code')
            }
        )
    )


class CustomerPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('password')
            }
        )
    )


class CustomerPasswordSetForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Customer
        fields = ('password',)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password"])
        if commit:
            customer.save()
        return customer


class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name')


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
    phone_number = forms.CharField(max_length=12,
                                   validators=[
                                       int_list_validator(message=_('only digits are accepted')),
                                       phone_number_validator
                                   ],
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'phone number'})
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

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data['username']
        user = ServiceProvider.objects.filter(
            Q(username=username) |
            Q(email=username) |
            Q(phone_number=username),
        ).first()

        if user and user.check_password(cleaned_data['password']):
            cleaned_data['user'] = user
            return cleaned_data

        raise ValidationError('username or password invalid!')
