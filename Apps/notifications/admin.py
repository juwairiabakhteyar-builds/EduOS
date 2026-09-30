from django.contrib import admin

from .models import Notification, NotificationRead


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "audience",
        "priority",
        "published",
        "created_by",
        "created_at",
    )
    list_filter = ("audience", "priority", "published")
    search_fields = ("title", "message")
    readonly_fields = ("created_at", "updated_at")


@admin.register(NotificationRead)
class NotificationReadAdmin(admin.ModelAdmin):
    list_display = ("notification", "user", "read_at")
    search_fields = (
        "notification__title",
        "user__username",
    )
    readonly_fields = ("read_at",)
