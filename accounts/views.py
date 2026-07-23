from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Apps.students.models import Student
from Apps.academics.models import AcademicLevel, Section

def home(request):

    User = get_user_model()

    return render(
        request,
        "home/home.html"
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
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

@login_required
def dashboard(request):

    recent_students = Student.objects.order_by("-id")[:5]

    print("Students Found:", recent_students.count())

    context = {
        "total_students": Student.objects.count(),
        "total_teachers": 0,
        "total_classes": AcademicLevel.objects.count(),
        "total_sections": Section.objects.count(),
        "recent_students": recent_students,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )