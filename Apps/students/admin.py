from django.contrib import admin

from .models import Student
from .forms import StudentForm


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    form = StudentForm

    list_display = (
        "student_id",
        "admission_number",
        "full_name",
        "academic_level",
        "section",
    )

    search_fields = (
        "student_id",
        "admission_number",
        "first_name",
        "last_name",
    )

    list_filter = (
        "academic_session",
        "academic_level",
        "section",
    )

    readonly_fields = (
        "student_id",
        "admission_number",
    )