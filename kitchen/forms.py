from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django.utils.translation import gettext_lazy as _

from kitchen.models import DishType, Dish


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
        label=_("Name:"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter name...",
            }
        ),
    )

    class Meta:
        model = DishType
        fields = "__all__"


class DishSearchForm(forms.Form):
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


class DishForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name:"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg mb-3",
                "placeholder": "Name"
            }
        ),
    )

    description = forms.CharField(
        label=_("Description:"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-lg mb-3",
                "placeholder": "A few words about this dish",
            }
        ),
    )

    price = forms.DecimalField(
        label=_("Price:"),
        widget=forms.NumberInput(
            attrs={
                "min": "0",
                "max": "100",
                "step": "0.01",
                "class": "form-control form-control-lg mb-3",
                "placeholder": "Price for 100g, $",
            }
        ),
    )

    dessert_type = forms.ModelChoiceField(
        label=_("Dish Type:"),
        queryset=DishType.objects.all(),
        empty_label="Select a dish type",
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-lg mb-3",
                "placeholder": "Choose a dish type.",
            }
        ),
    )

    cooks = forms.ModelMultipleChoiceField(
        label="Cooks:",
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input mb-3",
            }
        ),
    )

    image = forms.ImageField(
        label=_("Image:"),
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg mb-3",
                "placeholder": "Image"
            }
        ),
    )

    class Meta:
        model = Dish
        fields = "__all__"
