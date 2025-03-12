from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                # "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
            }
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
    )
