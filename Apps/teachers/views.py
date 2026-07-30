from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Teacher
from .forms import TeacherForm


def teacher_list(request):

    query = request.GET.get("q")

    teachers = Teacher.objects.all().order_by("teacher_id")

    if query:

        teachers = (
            teachers.filter(first_name__icontains=query)
            | teachers.filter(last_name__icontains=query)
            | teachers.filter(teacher_id__icontains=query)
            | teachers.filter(designation__icontains=query)
        )

    paginator = Paginator(
        teachers,
        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "teachers/teacher_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        },
    )


def teacher_create(request):

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            request.FILES,
        )

        print("=" * 60)
        print("POST RECEIVED")

        if form.is_valid():

            print("FORM IS VALID")

            teacher = form.save()

            print("=" * 60)
            print("Teacher Saved Successfully")
            print("Teacher ID:", teacher.teacher_id)
            print("=" * 60)

            messages.success(
                request,
                "Teacher added successfully."
            )

            return redirect(
                "teacher_list"
            )

        else:

            print("=" * 60)
            print("FORM ERRORS")
            print(form.errors.as_json())
            print("=" * 60)

    else:

        form = TeacherForm()

    return render(
        request,
        "teachers/teacher_create.html",
        {
            "form": form,
        },
    )


def teacher_detail(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk,
    )

    return render(
        request,
        "teachers/teacher_detail.html",
        {
            "teacher": teacher,
        },
    )


def teacher_update(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk,
    )

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            request.FILES,
            instance=teacher,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Teacher updated successfully."
            )

            return redirect(
                "teacher_detail",
                pk=teacher.pk,
            )

        else:

            print("=" * 60)
            print("UPDATE FORM ERRORS")
            print(form.errors.as_json())
            print("=" * 60)

    else:

        form = TeacherForm(
            instance=teacher,
        )

    return render(
        request,
        "teachers/teacher_create.html",
        {
            "form": form,
            "teacher": teacher,
        },
    )


def teacher_delete(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk,
    )

    if request.method == "POST":

        teacher.delete()

        messages.success(
            request,
            "Teacher deleted successfully."
        )

        return redirect(
            "teacher_list"
        )

    return render(
        request,
        "teachers/teacher_delete.html",
        {
            "teacher": teacher,
        },
    )