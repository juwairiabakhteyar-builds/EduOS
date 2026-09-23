from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.guardians.models import Guardian

from .models import Student


class StudentModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.session = AcademicSession.objects.create(
            name="2026-2027",
        )

        cls.level = AcademicLevel.objects.create(
            name="Class 5",
        )

        cls.section = Section.objects.create(
            name="A",
        )

        cls.guardian = Guardian.objects.create(
            first_name="Test",
            last_name="Guardian",
            relationship="Father",
            mobile_number="9876543210",
            email="guardian@example.com",
            occupation="Teacher",
        )

    def test_student_id_is_generated_automatically(self):
        student = Student.objects.create(
            first_name="Test",
            middle_name="Demo",
            last_name="Student",
            gender="Male",
            date_of_birth=date(2015, 5, 10),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
            guardian=self.guardian,
        )

        self.assertTrue(student.student_id.startswith("STU"))
        self.assertEqual(len(student.student_id), 9)

    def test_admission_number_is_generated_automatically(self):
        student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            gender="Female",
            date_of_birth=date(2015, 5, 10),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
            guardian=self.guardian,
        )

        current_year = date.today().year

        self.assertTrue(
            student.admission_number.startswith(
                f"ADM{current_year}"
            )
        )

    def test_full_name_includes_middle_name(self):
        student = Student.objects.create(
            first_name="Aisha",
            middle_name="Noor",
            last_name="Khan",
            gender="Female",
            date_of_birth=date(2014, 4, 20),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
            guardian=self.guardian,
        )

        self.assertEqual(
            student.full_name,
            "Aisha Noor Khan",
        )

    def test_full_name_without_middle_name(self):
        student = Student.objects.create(
            first_name="Aisha",
            middle_name="",
            last_name="Khan",
            gender="Female",
            date_of_birth=date(2014, 4, 20),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
            guardian=self.guardian,
        )

        self.assertEqual(
            student.full_name,
            "Aisha Khan",
        )


class StudentViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.session = AcademicSession.objects.create(
            name="2026-2027",
        )

        cls.level = AcademicLevel.objects.create(
            name="Class 5",
        )

        cls.section = Section.objects.create(
            name="A",
        )

        cls.guardian = Guardian.objects.create(
            first_name="Test",
            last_name="Guardian",
            relationship="Father",
            mobile_number="9876543210",
            email="guardian@example.com",
            occupation="Teacher",
        )

        cls.student = Student.objects.create(
            first_name="Aisha",
            last_name="Khan",
            gender="Female",
            date_of_birth=date(2014, 4, 20),
            academic_session=cls.session,
            academic_level=cls.level,
            section=cls.section,
            guardian=cls.guardian,
        )

    def test_student_list_page_loads(self):
        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Aisha Khan",
        )

    def test_student_detail_page_loads(self):
        response = self.client.get(
            reverse(
                "student_detail",
                kwargs={"pk": self.student.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            self.student.student_id,
        )

    def test_student_search_by_name(self):
        response = self.client.get(
            reverse("student_list"),
            {"q": "Aisha"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Aisha Khan",
        )

    def test_student_search_by_student_id(self):
        response = self.client.get(
            reverse("student_list"),
            {"q": self.student.student_id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Aisha Khan",
        )

    def test_sections_endpoint(self):
        response = self.client.get(
            reverse("get_sections")
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": self.section.id,
                    "name": "A",
                }
            ],
        )


class StudentFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.session = AcademicSession.objects.create(
            name="2026-2027",
        )

        cls.level = AcademicLevel.objects.create(
            name="Class 5",
        )

        cls.section = Section.objects.create(
            name="A",
        )

    def valid_form_data(self):
        return {
            "first_name": "Aisha",
            "middle_name": "Noor",
            "last_name": "Khan",
            "gender": "Female",
            "date_of_birth": "2014-04-20",
            "academic_session": self.session.pk,
            "academic_level": self.level.pk,
            "section": self.section.pk,
            "guardian_first_name": "Mohammad",
            "guardian_last_name": "Khan",
            "guardian_relationship": "Father",
            "guardian_mobile": "9876543210",
            "guardian_email": "father@example.com",
            "guardian_occupation": "Engineer",
        }

    def test_valid_student_form(self):
        from .forms import StudentForm

        form = StudentForm(
            data=self.valid_form_data()
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

    def test_invalid_guardian_mobile(self):
        from .forms import StudentForm

        data = self.valid_form_data()
        data["guardian_mobile"] = "12345"

        form = StudentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "guardian_mobile",
            form.errors,
        )

    def test_invalid_student_name(self):
        from .forms import StudentForm

        data = self.valid_form_data()
        data["first_name"] = "Aisha123"

        form = StudentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "first_name",
            form.errors,
        )

    def test_future_date_of_birth_is_rejected(self):
        from .forms import StudentForm

        data = self.valid_form_data()
        data["date_of_birth"] = "2099-01-01"

        form = StudentForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "date_of_birth",
            form.errors,
        )