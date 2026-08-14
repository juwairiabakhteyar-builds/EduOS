from django.db import models
from django.conf import settings

from Apps.students.models import Student

from Apps.academics.models import (
    AcademicSession,
    AcademicLevel,
    Section,
)


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
        ("Half Day", "Half Day"),
        ("Leave", "Leave"),
    ]

    # ------------------------------------------------------
    # STUDENT
    # ------------------------------------------------------

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    # ------------------------------------------------------
    # ACADEMIC INFORMATION
    # ------------------------------------------------------

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    academic_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # ------------------------------------------------------
    # ATTENDANCE INFORMATION
    # ------------------------------------------------------

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present",
    )

    remarks = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # MARKED BY
    # ------------------------------------------------------

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendance",
    )

    # ------------------------------------------------------
    # TIMESTAMPS
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    def save(self, *args, **kwargs):

        if self.student:

            self.academic_session = (
                self.student.academic_session
            )

            self.academic_level = (
                self.student.academic_level
            )

            self.section = (
                self.student.section
            )

        super().save(*args, **kwargs)

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:

        ordering = [
            "-attendance_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "attendance_date",
                ],
                name="unique_student_attendance_date",
            ),
        ]

        verbose_name = "Attendance"

        verbose_name_plural = "Attendance"

    # ------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"{self.student} - "
            f"{self.attendance_date} - "
            f"{self.status}"
        )