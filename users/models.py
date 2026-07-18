from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('school_admin', 'School Admin'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
        ('transport_manager', 'Transport Manager'),
        ('staff', 'Non Teaching Staff'),
        ('student', 'Student'),
        ('parent', 'Parent/Guardian'),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='student'
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"