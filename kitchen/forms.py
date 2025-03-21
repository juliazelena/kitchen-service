from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, \
    UserCreationForm
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from kitchen.models import DishType, Dish, Ingredient, Cook


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
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Name"
            }
        ),
    )

    description = forms.CharField(
        label=_("Description:"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
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
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Price for 100g, $",
            }
        ),
    )

    dish_type = forms.ModelChoiceField(
        label=_("Dish Type:"),
        queryset=DishType.objects.all(),
        empty_label="Select a dish type",
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-lg border border-primary mb-3",
                "placeholder": "Choose a dish type.",
            }
        ),
    )

    cooks = forms.ModelMultipleChoiceField(
        label="Cooks:",
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input order border-primary mb-3",
            }
        ),
    )

    ingredients = forms.ModelMultipleChoiceField(
        label="Ingredients:",
        queryset=Ingredient.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select form-select-lg border border-primary mb-3",
                "placeholder": "Choose ingredients.",
            }
        ),
    )

    image = forms.ImageField(
        label=_("Image:"),
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg mb-3 border border-pink-500 rounded-3 shadow-sm",
                "accept": "image/*",
                "style": "border-color: #ff69b4; padding: 10px; background-color: #fff3f8;",
            }
        ),
    )

    class Meta:
        model = Dish
        fields = "__all__"


class IngredientSearchForm(forms.Form):
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


class IngredientForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name:"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter name",
            }
        ),
    )

    class Meta:
        model = DishType
        fields = "__all__"


class CookCreationForm(UserCreationForm):
    username = UsernameField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter your username",
            }
        ),
    )
    years_of_experience = forms.IntegerField(
        initial=0,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Indicate years of experience",
            }
        ),
    )

    image = forms.ImageField(
        # initial="Image",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg mb-3",
                "accept": "image/*"
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter your first name",
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter your last name",
            }
        ),
    )

    password1 = forms.CharField(
        label=_("Password:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Enter your password",
            }
        )
    )

    password2 = forms.CharField(
        label=_("Confirm Password:"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
            "image",
        )

    def clean_years_of_experience(self):
        return validate_years_of_experience(
            self.cleaned_data["years_of_experience"]
        )


class CookUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField(
        initial=0,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Years of Experience",
            }
        ),
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg mb-3 border border-pink-500 rounded-3 shadow-sm",
                "accept": "image/*",
                "style": "border-color: #ff69b4; padding: 10px; background-color: #fff3f8;",
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "First Name",
            }
        ),
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border border-primary shadow-sm p-3",
                "placeholder": "Last Name",
            }
        ),
    )

    class Meta:
        model = Cook
        fields = ["years_of_experience", "first_name", "last_name", "image"]

    def clean_years_of_experience(self):
        return validate_years_of_experience(
            self.cleaned_data["years_of_experience"]
        )


def validate_years_of_experience(
        years_of_experience,
):
    if len(str(years_of_experience)) >= 3:
        raise ValidationError(
            "Years of experience should be 1 or 2 digital number"
        )
    elif years_of_experience < 0:
        raise ValidationError("Years of experience can't be negative")

    return years_of_experience


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Search by username",
            }
        ),
    )
