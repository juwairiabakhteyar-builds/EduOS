from django.db import models


class LeaveType(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    leave_name = models.CharField(
        max_length=100,
        unique=True,
    )

    leave_code = models.CharField(
        max_length=10,
        unique=True,
    )

    maximum_days = models.PositiveIntegerField(
        default=0,
    )

    is_paid = models.BooleanField(
        default=True,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["leave_name"]

        verbose_name = "Leave Type"

        verbose_name_plural = "Leave Types"

    def __str__(self):

        return f"{self.leave_name} ({self.leave_code})"