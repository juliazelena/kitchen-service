from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from kitchen.forms import UserLoginForm
from kitchen.models import Dish, DishType, Cook


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get(
            "remember_me"
        )  # get remember me data from cleaned_data of form
        if remember_me:
            self.request.session.set_expiry(10000)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("/accounts/login")


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html", context=context)
