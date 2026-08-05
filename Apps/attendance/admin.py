from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "person",
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
        "person__username",
        "person__first_name",
        "person__last_name",
    )

    ordering = (
        "-attendance_date",
        "-created_at",
    )

    date_hierarchy = "attendance_date"