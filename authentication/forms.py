# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation.trans_null import gettext_lazy


def validate_phone_number(phone_number):
    if len(phone_number) != 11 or not phone_number.isdigit():
        raise ValidationError(
            gettext_lazy("Phone number must have 11 digits")
        )

class LoginForm(forms.Form):
    phone_number_user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "09111111111",
                "class": "form-control"
            }
        ),
        validators=[validate_phone_number]
    )
    otp_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "OTP Code (Sent by SMS)",
                "class": "form-control"
            }
        ),
        required=False,
    )

class SignUpForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "First Name",
                "class": "form-control",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Last Name",
                "class": "form-control",
            }
        )
    )
    phone_number_user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "09111111111",
                "class": "form-control",
            }
        ),
        validators=[validate_phone_number]
    )
    agree_to_terms = forms.BooleanField(
        label='I agree to the <a href="/terms-and-conditions/" target="_blank" class="text-success">Terms and Conditions</a>',
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        error_messages={"required": "You must agree to the terms and conditions to register."},
    )
    subscription_code = forms.CharField(max_length=100, required=False)
