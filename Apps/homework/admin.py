from django.contrib import admin

from .models import HomeworkAssignment


@admin.register(HomeworkAssignment)
class HomeworkAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "teacher",
        "academic_level",
        "section",
        "assigned_date",
        "due_date",
        "is_published",
    )

    list_filter = (
        "academic_session",
        "academic_level",
        "section",
        "is_published",
        "assigned_date",
        "due_date",
    )

    search_fields = (
        "title",
        "subject",
        "description",
        "teacher__first_name",
        "teacher__last_name",
    )

    date_hierarchy = "due_date"

    ordering = (
        "-assigned_date",
        "-created_at",
    )