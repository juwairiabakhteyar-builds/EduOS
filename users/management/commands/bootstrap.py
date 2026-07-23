from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Bootstrap EduOS"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():

            User.objects.create_superuser(
                username="admin",
                email="admin@eduos.com",
                password="EduOS@123",
                role="super_admin",
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "✅ Super Admin created successfully."
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "⚠ Super Admin already exists."
                )
            )