from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "login.html")


@login_required
def home(request):

    user = request.user

    context = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

    return render(request, "home.html", context)


def logout_page(request):

    logout(request)

    return redirect("login")
