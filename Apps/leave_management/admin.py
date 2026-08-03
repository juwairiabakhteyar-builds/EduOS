from django.contrib import admin

from .models import LeaveType


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):

    list_display = (
        "leave_name",
        "leave_code",
        "maximum_days",
        "is_paid",
        "status",
    )

    list_filter = (
        "status",
        "is_paid",
    )

    search_fields = (
        "leave_name",
        "leave_code",
    )