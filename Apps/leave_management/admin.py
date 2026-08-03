from django.contrib import admin

from .models import LeaveType, LeaveApplication


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


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "applicant",
        "leave_type",
        "from_date",
        "to_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "leave_type",
    )

    search_fields = (
        "applicant__username",
        "leave_type__leave_name",
    )