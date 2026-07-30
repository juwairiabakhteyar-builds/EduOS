from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "teacher_id",
        "full_name",
        "designation",
        "mobile_number",
        "status",
    )

    search_fields = (
        "teacher_id",
        "first_name",
        "last_name",
        "mobile_number",
    )

    list_filter = (
        "status",
        "designation",
    )

    readonly_fields = (
        "teacher_id",
    )