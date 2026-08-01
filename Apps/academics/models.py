from django.db import models
from django.core.exceptions import ValidationError
import re


class AcademicSession(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True,
    )

    is_active = models.BooleanField(
        default=False,
    )

    def clean(self):

        pattern = r"^\d{4}-\d{4}$"

        if not re.fullmatch(pattern, self.name):
            raise ValidationError(
                {
                    "name":
                    "Session must be in the format YYYY-YYYY (Example: 2026-2027)."
                }
            )

        start_year = int(self.name[:4])
        end_year = int(self.name[5:])

        if end_year != start_year + 1:
            raise ValidationError(
                {
                    "name":
                    "End year must be exactly one year after the start year."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name