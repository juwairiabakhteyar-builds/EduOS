from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

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
        "gender",
    )

    readonly_fields = (
        "student_id",
        "admission_number",
    )