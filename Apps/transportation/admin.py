from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    RouteStop,
    StudentTransport,
    TransportAttendance,
    TransportRoute,
    Vehicle,
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "registration_number",
        "vehicle_type",
        "capacity",
        "driver_name",
        "route_name",
        "is_active",
    )
    list_filter = ("vehicle_type", "is_active")
    search_fields = (
        "name",
        "registration_number",
        "driver_name",
        "route_name",
    )


@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pickup_time",
        "drop_time",
        "fare",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ("route", "name", "stop_order", "pickup_time")
    list_filter = ("route",)
    search_fields = ("name", "route__name")
    ordering = ("route", "stop_order")


@admin.register(StudentTransport)
class StudentTransportAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "route",
        "pickup_stop",
        "vehicle",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("route", "vehicle", "is_active")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__student_id",
        "route__name",
    )


@admin.register(TransportAttendance)
class TransportAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "date",
        "status",
        "remarks",
    )
    list_filter = ("status", "date")
    search_fields = (
        "assignment__student__first_name",
        "assignment__student__last_name",
        "assignment__student__student_id",
    )
    date_hierarchy = "date"