from django.contrib import admin

from .models import Guardian


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "relationship",
        "mobile_number",
    )

    search_fields = (
        "first_name",
        "last_name",
        "mobile_number",
    )