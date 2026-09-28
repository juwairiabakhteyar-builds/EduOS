from django.db import models

# Create your models here.
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ("bus", "Bus"),
        ("van", "Van"),
        ("car", "Car"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=30, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default="bus")
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    driver_name = models.CharField(max_length=150, blank=True)
    driver_phone = models.CharField(max_length=20, blank=True)
    route_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["registration_number"]),
            models.Index(fields=["route_name"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.registration_number}"


class TransportRoute(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    drop_time = models.TimeField(null=True, blank=True)
    fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RouteStop(models.Model):
    route = models.ForeignKey(
        TransportRoute,
        on_delete=models.CASCADE,
        related_name="stops",
    )
    name = models.CharField(max_length=150)
    stop_order = models.PositiveIntegerField(default=1)
    pickup_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["route", "stop_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["route", "stop_order"],
                name="unique_route_stop_order",
            )
        ]

    def __str__(self):
        return f"{self.route.name} - {self.name}"


class StudentTransport(models.Model):
    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="transport_assignment",
    )
    route = models.ForeignKey(
        TransportRoute,
        on_delete=models.PROTECT,
        related_name="student_assignments",
    )
    pickup_stop = models.ForeignKey(
        RouteStop,
        on_delete=models.PROTECT,
        related_name="student_pickups",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="student_assignments",
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["student__first_name", "student__last_name"]

    def __str__(self):
        return f"{self.student} - {self.route}"


class TransportAttendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
    ]

    assignment = models.ForeignKey(
        StudentTransport,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date", "assignment__student__first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "date"],
                name="unique_transport_attendance",
            )
        ]

    def __str__(self):
        return f"{self.assignment.student} - {self.date} - {self.status}"