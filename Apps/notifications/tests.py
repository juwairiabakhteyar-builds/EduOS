from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notification, NotificationRead

User = get_user_model()


class NotificationTests(TestCase):

    def setUp(self):
        self.school = None

        self.admin = User.objects.create_user(
            username="notifyadmin",
            password="pass12345",
            role="school_admin",
        )

        self.student = User.objects.create_user(
            username="notifystudent",
            password="pass12345",
            role="student",
        )

        self.teacher = User.objects.create_user(
            username="notifyteacher",
            password="pass12345",
            role="teacher",
        )

        self.notification = Notification.objects.create(
            title="School Holiday",
            message="School will remain closed tomorrow.",
            priority="important",
            audience="all",
            created_by=self.admin,
        )

    def test_notification_list_requires_login(self):
        response = self.client.get(reverse("notifications:list"))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_create_notification(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("notifications:create"),
            {
                "title": "Parent Meeting",
                "message": "Meeting at 10 AM.",
                "priority": "normal",
                "audience": "parents",
                "published": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Notification.objects.filter(title="Parent Meeting").exists()
        )

    def test_student_can_see_all_notification(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("notifications:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "School Holiday")

    def test_teacher_can_see_all_notification(self):
        self.client.force_login(self.teacher)

        response = self.client.get(reverse("notifications:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "School Holiday")

    def test_student_cannot_create_notification(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("notifications:create"))

        self.assertRedirects(
            response,
            reverse("notifications:list"),
        )

    def test_opening_notification_marks_it_read(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse(
                "notifications:detail",
                kwargs={"pk": self.notification.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            NotificationRead.objects.filter(
                notification=self.notification,
                user=self.student,
            ).exists()
        )

    def test_duplicate_read_record_is_not_created(self):
        NotificationRead.objects.create(
            notification=self.notification,
            user=self.student,
        )

        self.client.force_login(self.student)

        self.client.get(
            reverse(
                "notifications:detail",
                kwargs={"pk": self.notification.pk},
            )
        )

        self.assertEqual(
            NotificationRead.objects.filter(
                notification=self.notification,
                user=self.student,
            ).count(),
            1,
        )
