from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Bootstrap EduOS"


    def handle(self, *args, **kwargs):

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@eduos.com",
                "role": "super_admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )

        user.email = "admin@eduos.com"
        user.role = "super_admin"
        user.is_staff = True
        user.is_superuser = True
        user.set_password("EduOS@123")
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Super Admin is ready."
            )
        )

    else:

    self.stdout.write(
        self.style.WARNING(
        "⚠ Super Admin already exists."
        )
    )