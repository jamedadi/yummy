from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer


class CustomerLoginRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11,
                                   min_length=11,
                                   validators=[int_list_validator(message=_('only digits are accepted'))],
                                   error_messages={'min_length': _('phone number must have 11 digits')},
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
