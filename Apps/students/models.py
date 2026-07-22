from django.db import models

from Apps.academics.models import (
    AcademicSession,
    AcademicLevel,
    Section,
)

from Apps.guardians.models import Guardian

def __str__(self):

        return f"{self.academic_level} - {self.name}"

class Student(models.Model):

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    admission_number = models.CharField(
        max_length=30,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=20
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

    academic_level= models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT
    )

    guardian = models.ForeignKey(
    Guardian,
    on_delete=models.PROTECT,
    related_name="students",
    null=True,
    blank=True,
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.student_id} - {self.first_name} {self.last_name}"