from django.core.exceptions import ValidationError
from django.db import models

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.teachers.models import Teacher


class HomeworkAssignment(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="homework_assignments",
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="homework_assignments",
    )
    academic_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT,
        related_name="homework_assignments",
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="homework_assignments",
    )
    assigned_date = models.DateField()
    due_date = models.DateField()
    attachment = models.FileField(
        upload_to="homework/attachments/",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-assigned_date", "-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "academic_session",
                    "academic_level",
                    "section",
                ]
            ),
            models.Index(fields=["due_date"]),
            models.Index(fields=["is_published"]),
        ]

    def clean(self):
        if (
            self.assigned_date
            and self.due_date
            and self.due_date < self.assigned_date
        ):
            raise ValidationError(
                {
                    "due_date": (
                        "Due date cannot be earlier than the assigned date."
                    )
                }
            )

    def __str__(self):
        return f"{self.title} - {self.subject}"
