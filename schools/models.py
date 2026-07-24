from django.db import models

# Create your models here.
from django.db import models


class School(models.Model):

    name = models.CharField(
        max_length=200
    )

    address = models.TextField(
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    established_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name