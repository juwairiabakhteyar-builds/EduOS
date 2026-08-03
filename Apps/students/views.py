from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from Apps.academics.models import Section
from Apps.guardians.models import Guardian

from .forms import StudentForm
from .models import Student

from django.contrib import messages

def student_list(request):

    query = request.GET.get("q")

    students = Student.objects.all().order_by("student_id")

    if query:
        students = (
            students.filter(first_name__icontains=query)
            | students.filter(last_name__icontains=query)
            | students.filter(student_id__icontains=query)
            | students.filter(admission_number__icontains=query)
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
                    "Student admitted successfully."
                )

            return render(
                request,
                "students/student_list.html",
                {
                    "page_obj": Paginator(
                        Student.objects.all().order_by("student_id"),
                        10,
                    ).get_page(1),
                    "query": "",
                },
            )

        else:

            print(form.errors)

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
            print("===== EDIT FORM DATA =====")
            print(form.cleaned_data)
            print("==========================")

            student = form.save(commit=False)

            guardian = student.guardian

            guardian.first_name = form.cleaned_data["guardian_first_name"]
            guardian.last_name = form.cleaned_data["guardian_last_name"]
            guardian.relationship = form.cleaned_data["guardian_relationship"]
            guardian.mobile_number = form.cleaned_data["guardian_mobile"]
            guardian.email = form.cleaned_data["guardian_email"]
            guardian.occupation = form.cleaned_data["guardian_occupation"]

            guardian.save()
            print("Guardian saved:", guardian.mobile_number)

            student.save()

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
            initial={
                "guardian_first_name": student.guardian.first_name,
                "guardian_last_name": student.guardian.last_name,
                "guardian_relationship": student.guardian.relationship,
                "guardian_mobile": student.guardian.mobile_number,
                "guardian_email": student.guardian.email,
                "guardian_occupation": student.guardian.occupation,
            },
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

def get_sections(request):

    level_id = request.GET.get("academic_level")

    if not level_id:
        return JsonResponse([], safe=False)

    sections = Section.objects.filter(
        academic_level_id=level_id
    ).order_by("name")

    data = []

    for section in sections:

        data.append(
            {
                "id": section.id,
                "name": section.name,
            }
        )

    return JsonResponse(
        data,
        safe=False,
    )