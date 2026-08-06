from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "attendance_date",
        "status",
        "marked_by",
        "created_at",
    )

    list_filter = (
        "status",
        "attendance_date",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
        "student__admission_number",
    )

    ordering = (
        "-attendance_date",
        "-created_at",
    )

    date_hierarchy = "attendance_date"