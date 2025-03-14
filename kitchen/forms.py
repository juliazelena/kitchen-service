from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django.utils.translation import gettext_lazy as _

from kitchen.models import DishType


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

class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Search by name",
            }
        ),
    )

class DishTypeForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name*:"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg mb-3",
                "placeholder": "Name"
            }
        ),
    )

    class Meta:
        model = DishType
        fields = "__all__"
