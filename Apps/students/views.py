from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import StudentForm
from .models import Student


def student_list(request):

    query = request.GET.get("q")

    students = Student.objects.all()

    if query:
        students = students.filter(
            first_name__icontains=query
        ) | students.filter(
            last_name__icontains=query
        ) | students.filter(
            student_id__icontains=query
        ) | students.filter(
            admission_number__icontains=query
        )

    paginator = Paginator(students, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "students/student_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        },
    )


def student_create(request):

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student added successfully."
            )

            return redirect("student_list")

    else:

        form = StudentForm()

    return render(
        request,
        "students/student_create.html",
        {
            "form": form,
        },
    )


def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk,
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
        },
    )


def student_update(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk,
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect(
                "student_detail",
                pk=student.pk,
            )

    else:

        form = StudentForm(
            instance=student,
        )

    return render(
        request,
        "students/student_create.html",
        {
            "form": form,
            "student": student,
        },
    )


def student_delete(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk,
    )

    if request.method == "POST":

        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "students/student_delete.html",
        {
            "student": student,
        },
    )