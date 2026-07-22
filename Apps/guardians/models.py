from django.db import models


class Guardian(models.Model):

    RELATIONSHIP_CHOICES = [
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Guardian", "Guardian"),
        ("Other", "Other"),
    ]

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES
    )

    mobile_number = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    occupation = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.first_name} {self.last_name} ({self.relationship})"