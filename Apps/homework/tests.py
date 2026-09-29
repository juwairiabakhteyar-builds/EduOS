from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.teachers.models import Teacher

from .forms import HomeworkAssignmentForm
from .models import HomeworkAssignment


class HomeworkAssignmentModelTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(
            name="A",
        )

        self.teacher = Teacher.objects.create(
            first_name="Test",
            last_name="Teacher",
            gender="Male",
            date_of_birth=date(1985, 1, 1),
            mobile_number="9876543210",
            email="teacher@example.com",
            qualification="M.Ed",
            experience=5,
            joining_date=date(2020, 1, 1),
            designation="Teacher",
        )

    def create_assignment(self, **kwargs):
        data = {
            "title": "Algebra Practice",
            "subject": "Mathematics",
            "description": "Complete exercises 1 to 10.",
            "teacher": self.teacher,
            "academic_session": self.session,
            "academic_level": self.level,
            "section": self.section,
            "assigned_date": date.today(),
            "due_date": date.today() + timedelta(days=3),
            "is_published": True,
        }

        data.update(kwargs)

        return HomeworkAssignment.objects.create(**data)

    def test_assignment_string(self):
        assignment = self.create_assignment()

        self.assertEqual(
            str(assignment),
            "Algebra Practice - Mathematics",
        )

    def test_assignment_creation(self):
        assignment = self.create_assignment()

        self.assertEqual(
            assignment.teacher,
            self.teacher,
        )
        self.assertEqual(
            assignment.academic_level,
            self.level,
        )
        self.assertEqual(
            assignment.section,
            self.section,
        )
        self.assertTrue(assignment.is_published)

    def test_invalid_date_range(self):
        assignment = self.create_assignment(
            due_date=date.today() - timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            assignment.full_clean()


class HomeworkAssignmentFormTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(
            name="A",
        )

        self.teacher = Teacher.objects.create(
            first_name="Form",
            last_name="Teacher",
            gender="Female",
            date_of_birth=date(1986, 1, 1),
            mobile_number="9876543211",
            email="formteacher@example.com",
            qualification="M.A.",
            experience=3,
            joining_date=date(2021, 1, 1),
            designation="Teacher",
        )

    def form_data(self, **overrides):
        data = {
            "title": "Science Project",
            "subject": "Science",
            "description": "Complete the assigned project.",
            "teacher": self.teacher.pk,
            "academic_session": self.session.pk,
            "academic_level": self.level.pk,
            "section": self.section.pk,
            "assigned_date": date.today(),
            "due_date": date.today() + timedelta(days=5),
            "is_published": "on",
        }

        data.update(overrides)

        return data

    def test_valid_form(self):
        form = HomeworkAssignmentForm(
            data=self.form_data(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors,
        )

    def test_form_rejects_invalid_date_range(self):
        form = HomeworkAssignmentForm(
            data=self.form_data(
                due_date=date.today() - timedelta(days=1),
            ),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("due_date", form.errors)