from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .forms import TeacherForm
from .models import Teacher


class TeacherTests(TestCase):

    def setUp(self):
        self.teacher = Teacher.objects.create(
            first_name="Amit",
            middle_name="Kumar",
            last_name="Sharma",
            gender="Male",
            date_of_birth=date(1990, 5, 10),
            mobile_number="9876543210",
            email="amit@example.com",
            qualification="M.Ed",
            experience=5,
            joining_date=date(2020, 6, 1),
            designation="Senior Teacher",
            status="Active",
        )

    def test_teacher_id_generated(self):
        self.assertTrue(
            self.teacher.teacher_id.startswith("TCH")
        )
        self.assertEqual(
            len(self.teacher.teacher_id),
            9,
        )

    def test_teacher_full_name(self):
        self.assertEqual(
            self.teacher.full_name,
            "Amit Kumar Sharma",
        )

    def test_teacher_str(self):
        self.assertIn(
            self.teacher.teacher_id,
            str(self.teacher),
        )
        self.assertIn(
            "Amit Kumar Sharma",
            str(self.teacher),
        )

    def test_teacher_list_page(self):
        response = self.client.get(
            reverse("teacher_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amit")
        self.assertContains(response, "Sharma")
        self.assertContains(
            response,
            self.teacher.teacher_id,
        )

    def test_teacher_search(self):
        response = self.client.get(
            reverse("teacher_list"),
            {"q": "Amit"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amit")

    def test_teacher_create(self):
        response = self.client.post(
            reverse("teacher_create"),
            {
                "first_name": "Sara",
                "middle_name": "",
                "last_name": "Khan",
                "gender": "Female",
                "date_of_birth": "1992-08-15",
                "mobile_number": "9123456789",
                "email": "sara@example.com",
                "qualification": "M.A.",
                "experience": 3,
                "joining_date": "2022-07-01",
                "designation": "Teacher",
                "address": "Darbhanga",
                "status": "Active",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Teacher.objects.filter(
                email="sara@example.com"
            ).exists()
        )

    def test_teacher_update(self):
        response = self.client.post(
            reverse(
                "teacher_update",
                kwargs={"pk": self.teacher.pk},
            ),
            {
                "first_name": "Amit",
                "middle_name": "Kumar",
                "last_name": "Updated",
                "gender": "Male",
                "date_of_birth": "1990-05-10",
                "mobile_number": "9876543210",
                "email": "amit@example.com",
                "qualification": "M.Ed",
                "experience": 6,
                "joining_date": "2020-06-01",
                "designation": "Head Teacher",
                "address": "",
                "status": "Active",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.teacher.refresh_from_db()

        self.assertEqual(
            self.teacher.last_name,
            "Updated",
        )
        self.assertEqual(
            self.teacher.experience,
            6,
        )

    def test_teacher_delete(self):
        response = self.client.post(
            reverse(
                "teacher_delete",
                kwargs={"pk": self.teacher.pk},
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Teacher.objects.filter(
                pk=self.teacher.pk
            ).exists()
        )

    def test_teacher_form_rejects_invalid_mobile(self):
        form = TeacherForm(
            data={
                "first_name": "Test",
                "middle_name": "",
                "last_name": "Teacher",
                "gender": "Male",
                "date_of_birth": "1990-05-10",
                "mobile_number": "12345",
                "email": "invalidmobile@example.com",
                "qualification": "M.Ed",
                "experience": 1,
                "joining_date": "2024-01-01",
                "designation": "Teacher",
                "address": "",
                "status": "Active",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "mobile_number",
            form.errors,
        )
