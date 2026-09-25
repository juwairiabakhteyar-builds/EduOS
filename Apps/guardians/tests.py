from django.test import TestCase
from django.urls import reverse

from .models import Guardian


class GuardianTests(TestCase):

    def setUp(self):
        self.guardian = Guardian.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            relationship="Father",
            mobile_number="9876543210",
            email="rahul@example.com",
            occupation="Engineer",
        )

    def test_guardian_str(self):
        self.assertEqual(
            str(self.guardian),
            "Rahul Kumar (Father)",
        )

    def test_guardian_list_page(self):
        response = self.client.get(reverse("guardian_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahul")
        self.assertContains(response, "Kumar")

    def test_guardian_search(self):
        response = self.client.get(
            reverse("guardian_list"),
            {"q": "Rahul"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahul")

    def test_guardian_relationship_filter(self):
        response = self.client.get(
            reverse("guardian_list"),
            {"relationship": "Father"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahul")

    def test_guardian_create(self):
        response = self.client.post(
            reverse("guardian_create"),
            {
                "first_name": "Amit",
                "last_name": "Sharma",
                "relationship": "Mother",
                "mobile_number": "9123456789",
                "email": "amit@example.com",
                "occupation": "Teacher",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Guardian.objects.filter(
                first_name="Amit",
                last_name="Sharma",
            ).exists()
        )

    def test_guardian_update(self):
        response = self.client.post(
            reverse(
                "guardian_update",
                kwargs={"pk": self.guardian.pk},
            ),
            {
                "first_name": "Rahul Updated",
                "last_name": "Kumar",
                "relationship": "Father",
                "mobile_number": "9876543210",
                "email": "rahul.updated@example.com",
                "occupation": "Manager",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.guardian.refresh_from_db()

        self.assertEqual(
            self.guardian.email,
            "rahul.updated@example.com",
        )

    def test_guardian_delete(self):
        response = self.client.post(
            reverse(
                "guardian_delete",
                kwargs={"pk": self.guardian.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Guardian.objects.filter(
                pk=self.guardian.pk
            ).exists()
        )
