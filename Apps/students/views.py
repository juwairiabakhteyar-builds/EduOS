from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Apps.academics.models import Section
from Apps.guardians.models import Guardian

from .forms import StudentForm
from .models import Student


def student_list(request):
    query = request.GET.get("q", "").strip()

    students = (
        Student.objects
        .select_related(
            "academic_session",
            "academic_level",
            "section",
            "guardian",
        )
        .order_by("student_id")
    )

    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(student_id__icontains=query)
            | Q(admission_number__icontains=query)
            | Q(guardian__first_name__icontains=query)
            | Q(guardian__last_name__icontains=query)
            | Q(guardian__mobile_number__icontains=query)
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


@transaction.atomic
def student_create(request):

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            guardian = Guardian.objects.create(
                first_name=form.cleaned_data["guardian_first_name"],
                last_name=form.cleaned_data["guardian_last_name"],
                relationship=form.cleaned_data["guardian_relationship"],
                mobile_number=form.cleaned_data["guardian_mobile"],
                email=form.cleaned_data["guardian_email"],
                occupation=form.cleaned_data["guardian_occupation"],
            )

            student = form.save(commit=False)
            student.guardian = guardian
            student.save()

            messages.success(
                request,
                f"{student.full_name} was admitted successfully.",
            )

            return redirect(
                "student_detail",
                pk=student.pk,
            )

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_create.html",
        {
            "form": form,
            "page_mode": "create",
        },
    )


def student_detail(request, pk):

    student = get_object_or_404(
        Student.objects.select_related(
            "academic_session",
            "academic_level",
            "section",
            "guardian",
        ),
        pk=pk,
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
        },
    )


@transaction.atomic
def student_update(request, pk):

    student = get_object_or_404(
        Student.objects.select_related("guardian"),
        pk=pk,
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student,
        )

        if form.is_valid():

            student = form.save(commit=False)

            guardian = student.guardian

            if guardian:
                guardian.first_name = (
                    form.cleaned_data["guardian_first_name"]
                )
                guardian.last_name = (
                    form.cleaned_data["guardian_last_name"]
                )
                guardian.relationship = (
                    form.cleaned_data["guardian_relationship"]
                )
                guardian.mobile_number = (
                    form.cleaned_data["guardian_mobile"]
                )
                guardian.email = (
                    form.cleaned_data["guardian_email"]
                )
                guardian.occupation = (
                    form.cleaned_data["guardian_occupation"]
                )

                guardian.save()

            else:
                guardian = Guardian.objects.create(
                    first_name=form.cleaned_data["guardian_first_name"],
                    last_name=form.cleaned_data["guardian_last_name"],
                    relationship=form.cleaned_data["guardian_relationship"],
                    mobile_number=form.cleaned_data["guardian_mobile"],
                    email=form.cleaned_data["guardian_email"],
                    occupation=form.cleaned_data["guardian_occupation"],
                )

                student.guardian = guardian

            student.save()

            messages.success(
                request,
                f"{student.full_name} was updated successfully.",
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
            "page_mode": "edit",
        },
    )


def student_delete(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk,
    )

    if request.method == "POST":

        student_name = student.full_name

        student.delete()

        messages.success(
            request,
            f"{student_name} was deleted successfully.",
        )

        return redirect("student_list")

    return render(
        request,
        "students/student_delete.html",
        {
            "student": student,
        },
    )


def get_sections(request):

    sections = Section.objects.all().order_by("name")

    data = [
        {
            "id": section.id,
            "name": section.name,
        }
        for section in sections
    ]

    return JsonResponse(data, safe=False)