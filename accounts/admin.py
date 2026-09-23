from django.contrib import admin

from .models import AccessRequest

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):

    list_display = (
        "school_name",
        "contact_person",
        "email",
        "requested_role",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "requested_role",
        "created_at",
    )

    search_fields = (
        "school_name",
        "contact_person",
        "email",
        "phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )
