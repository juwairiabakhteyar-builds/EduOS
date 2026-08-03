from django.db import models
from django.conf import settings

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

    from django.conf import settings


class LeaveApplication(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_applications",
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    from_date = models.DateField()

    to_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    remarks = models.TextField(
        blank=True,
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leave_applications",
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Leave Application"

        verbose_name_plural = "Leave Applications"

    def __str__(self):

        return (
            f"{self.applicant.username} - "
            f"{self.leave_type.leave_name}"
        )