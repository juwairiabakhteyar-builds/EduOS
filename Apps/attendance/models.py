from django.db import models
from django.conf import settings


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
        ("Half Day", "Half Day"),
        ("Leave", "Leave"),
    ]

    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present",
    )

    remarks = models.TextField(
        blank=True,
    )

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendance",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-attendance_date"]

        unique_together = (
            "person",
            "attendance_date",
        )

        verbose_name = "Attendance"

        verbose_name_plural = "Attendance"

    def __str__(self):

        return (
            f"{self.person.username} - "
            f"{self.attendance_date} - "
            f"{self.status}"
        )