from django.shortcuts import render

from Apps.students.models import Student
from Apps.academics.models import AcademicLevel, Section


def dashboard(request):

    total_students = Student.objects.count()

    total_teachers = 0

    total_classes = AcademicLevel.objects.count()

    total_sections = Section.objects.count()

    recent_students = Student.objects.order_by("-id")[:5]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_classes": total_classes,
            "total_sections": total_sections,
            "recent_students": recent_students,
        },
    )