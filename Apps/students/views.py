from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentForm
from .models import Student


def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        "students/student_list.html",
        {
            "students": students
        }
    )


def student_create(request):

    if request.method == "POST":

        form = StudentForm(
        request.POST,
        request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("student_list")

    else:

        form = StudentForm()

    return render(
        request,
        "students/student_create.html",
        {
            "form": form
        }
    )

from django.shortcuts import get_object_or_404


def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student
        }
    )

def student_update(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_create.html",
        {
            "form": form
        }
    )

def student_delete(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        student.delete()

        return redirect("student_list")

    return render(
        request,
        "students/student_delete.html",
        {
            "student": student
        }
    )