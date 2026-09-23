from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def home(request):
    return render(
        request,
        "home/home.html"
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "authentication/login.html"
    )


def authority(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(
                request,
                "Please enter both username and password."
            )
            return render(
                request,
                "authentication/authority.html"
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            messages.error(
                request,
                "Invalid authority credentials."
            )
            return render(
                request,
                "authentication/authority.html"
            )

        if not user.is_active:
            messages.error(
                request,
                "Your account is currently inactive. Please contact your school administrator."
            )
            return render(
                request,
                "authentication/authority.html"
            )

        if user.role not in [
            "super_admin",
            "school_admin",
            "principal",
        ]:
            messages.error(
                request,
                "You do not have authority access."
            )
            return render(
                request,
                "authentication/authority.html"
            )

        login(request, user)
        return redirect("dashboard")

    return render(
        request,
        "authentication/authority.html"
    )