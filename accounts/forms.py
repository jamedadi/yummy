from django import forms
from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _


class CustomerLoginRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=10,
                                   min_length=10,
                                   validators=[int_list_validator(message=_('only digits are accepted'))],
                                   error_messages={'min_length': _('phone number must have 10 digits')},
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'phone number'})
                                   )


class CustomerCodeConfirmForm(forms.Form):
    class ConfirmationPhoneNumberForm(forms.Form):
        code = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('confirmation code')
                }
            )
        )
