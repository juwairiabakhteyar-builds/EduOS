import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():

    User.objects.create_superuser(
        username="admin",
        email="admin@eduos.com",
        password="EduOS@123",
        role="super_admin"
    )

    print("✅ Super Admin Created")

else:

    print("✅ Super Admin Already Exists")