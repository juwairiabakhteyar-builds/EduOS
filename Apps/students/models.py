from django.db import models
import datetime
import re

from Apps.academics.models import (
    AcademicSession,
    AcademicLevel,
    Section,
)

from Apps.guardians.models import Guardian


class Student(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender", "Transgender"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False,
    )

    admission_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
    )

    first_name = models.CharField(
        max_length=100
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    photo = models.ImageField(
        upload_to="students/photos/",
        blank=True,
        null=True
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT
    )

    academic_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )

    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["student_id"]

    @property
    def full_name(self):
        return (
            f"{self.first_name} {self.middle_name} {self.last_name}"
            .replace("  ", " ")
            .strip()
        )

    def save(self, *args, **kwargs):

        import datetime
        import re

        # -----------------------------
        # Auto Student ID
        # -----------------------------
        if not self.student_id:

            max_number = 0

            for student in Student.objects.exclude(pk=self.pk):

                sid = student.student_id or ""

                match = re.fullmatch(r"STU(\d+)", sid)

                if match:
                    number = int(match.group(1))
                    max_number = max(max_number, number)

            self.student_id = f"STU{max_number + 1:06d}"

        # -----------------------------
        # Auto Admission Number
        # -----------------------------
        if not self.admission_number:

            year = datetime.date.today().year

            max_number = 0

            for student in Student.objects.exclude(pk=self.pk):

                adm = student.admission_number or ""

                match = re.fullmatch(rf"ADM{year}(\d+)", adm)

                if match:
                    number = int(match.group(1))
                    max_number = max(max_number, number)

            self.admission_number = f"ADM{year}{max_number + 1:03d}"

        super().save(*args, **kwargs)