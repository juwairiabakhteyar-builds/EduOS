from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from schools.models import School

from Apps.academics.models import (
    AcademicSession,
    AcademicLevel,
    Section,
)

from Apps.guardians.models import Guardian


class Command(BaseCommand):
    help = "Bootstrap EduOS"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # -----------------------------
        # Super Admin
        # -----------------------------
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@eduos.com",
                "role": "super_admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = "admin@eduos.com"
        user.role = "super_admin"
        user.is_staff = True
        user.is_superuser = True
        user.set_password("EduOS@123")
        user.save()

        self.stdout.write(
            self.style.SUCCESS("✓ Super Admin is ready.")
        )

        # -----------------------------
        # Demo School
        # -----------------------------
        School.objects.get_or_create(
            name="EduOS Demo School",
            defaults={
                "address": "Demo City",
                "phone_number": "9999999999",
                "email": "demo@eduos.com",
                "established_year": 2020,
            },
        )

        self.stdout.write(
            self.style.SUCCESS("✓ Demo School ready.")
        )

        # -----------------------------
        # Academic Session
        # -----------------------------
        AcademicSession.objects.get_or_create(
            name="2026-2027",
            defaults={
                "is_active": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS("✓ Academic Session ready.")
        )

        # -----------------------------
        # Academic Levels
        # -----------------------------

        levels = [
            "Nursery",
            "LKG",
            "UKG",
        ]

        for i in range(1, 13):
            levels.append(str(i))

        for level_name in levels:
            AcademicLevel.objects.get_or_create(
                name=level_name
            )

        self.stdout.write(
            self.style.SUCCESS("✓ Academic Levels ready.")
        )

        # -----------------------------
        # Sections
        # -----------------------------
        for level in AcademicLevel.objects.all():
            for section_name in ["A", "B", "C"]:
                Section.objects.get_or_create(
                    academic_level=level,
                    name=section_name,
                )

        self.stdout.write(
            self.style.SUCCESS("✓ Sections ready.")
        )

        # -----------------------------
        # Demo Guardian
        # -----------------------------
        Guardian.objects.get_or_create(
            mobile_number="9999999999",
            defaults={
                "first_name": "Demo",
                "last_name": "Guardian",
                "relationship": "Father",
                "email": "guardian@eduos.com",
                "occupation": "Engineer",
            },
        )

        self.stdout.write(
            self.style.SUCCESS("✓ Demo Guardian ready.")
        )