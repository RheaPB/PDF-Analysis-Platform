from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError




def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is not None:
            login(request, user)
            return redirect("/app/")  # ✅ IMPORTANT
        else:
            return render(
                request,
                "registration/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "registration/login.html")



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.create_user(
                username=username,
                password=password
            )
        except IntegrityError:
            return render(
                request,
                "registration/register.html",
                {"error": "Username already exists"}
            )

        return redirect("/login/")

    return render(request, "registration/register.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("/login/")
