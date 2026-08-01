from django.db import models


class AcademicSession(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True
    )

    is_active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name


class AcademicLevel(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

class Section(models.Model):

    name = models.CharField(
        max_length=10,
    )

    academic_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    class Meta:

        ordering = ["name"]

        unique_together = (
            "academic_level",
            "name",
        )

    def __str__(self):
        return self.name