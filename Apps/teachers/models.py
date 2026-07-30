from django.db import models

# Create your models here.
from django.db import models


class Teacher(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender", "Transgender"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    teacher_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
    )

    date_of_birth = models.DateField()

    mobile_number = models.CharField(
        max_length=10,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    qualification = models.CharField(
        max_length=150,
    )

    experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience in years",
    )

    joining_date = models.DateField()

    designation = models.CharField(
        max_length=100,
    )

    photo = models.ImageField(
        upload_to="teachers/photos/",
        blank=True,
        null=True,
    )

    address = models.TextField(
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
        ordering = ["teacher_id"]

    @property
    def full_name(self):
        return (
            f"{self.first_name} "
            f"{self.middle_name} "
            f"{self.last_name}"
        ).replace("  ", " ").strip()

    def save(self, *args, **kwargs):

        if not self.teacher_id:

            last_number = 0

            for teacher in Teacher.objects.all():

                if (
                    teacher.teacher_id
                    and teacher.teacher_id.startswith("TCH")
                ):

                    try:
                        number = int(teacher.teacher_id[3:])

                        if number > last_number:
                            last_number = number

                    except ValueError:
                        continue

            self.teacher_id = f"TCH{last_number + 1:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"