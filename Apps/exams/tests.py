from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.exams.models import Exam, ExamResult, ExamSubject
from Apps.students.models import Student


class ExamModelTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

    def test_exam_rejects_invalid_date_range(self):
        exam = Exam(
            name="Mid Term",
            academic_session=self.session,
            academic_level=self.level,
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 10),
        )

        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test_exam_string_representation(self):
        exam = Exam.objects.create(
            name="Mid Term",
            academic_session=self.session,
            academic_level=self.level,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 20),
        )

        self.assertEqual(
            str(exam),
            "Mid Term - Class 10 - 2026-2027",
        )


class ExamSubjectModelTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(name="A")

        self.exam = Exam.objects.create(
            name="Mid Term",
            academic_session=self.session,
            academic_level=self.level,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 20),
        )

    def test_subject_rejects_passing_marks_above_maximum(self):
        subject = ExamSubject(
            exam=self.exam,
            name="Mathematics",
            exam_date=date(2026, 9, 12),
            max_marks=100,
            passing_marks=110,
        )

        with self.assertRaises(ValidationError):
            subject.full_clean()

    def test_subject_rejects_date_outside_exam_period(self):
        subject = ExamSubject(
            exam=self.exam,
            name="Mathematics",
            exam_date=date(2026, 9, 25),
            max_marks=100,
            passing_marks=33,
        )

        with self.assertRaises(ValidationError):
            subject.full_clean()


class ExamResultModelTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(name="A")

        self.exam = Exam.objects.create(
            name="Mid Term",
            academic_session=self.session,
            academic_level=self.level,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 20),
        )

        self.subject = ExamSubject.objects.create(
            exam=self.exam,
            name="Mathematics",
            exam_date=date(2026, 9, 12),
            max_marks=100,
            passing_marks=33,
        )

        self.student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            date_of_birth=date(2012, 1, 15),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
        )

    def test_result_rejects_negative_marks(self):
        result = ExamResult(
            student=self.student,
            subject=self.subject,
            marks_obtained=-1,
        )

        with self.assertRaises(ValidationError):
            result.full_clean()

    def test_result_rejects_marks_above_maximum(self):
        result = ExamResult(
            student=self.student,
            subject=self.subject,
            marks_obtained=101,
        )

        with self.assertRaises(ValidationError):
            result.full_clean()

    def test_result_pass_status(self):
        result = ExamResult.objects.create(
            student=self.student,
            subject=self.subject,
            marks_obtained=75,
        )

        self.assertTrue(result.is_passed)


class ExamViewTests(TestCase):

    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(name="A")

        self.exam = Exam.objects.create(
            name="Mid Term",
            academic_session=self.session,
            academic_level=self.level,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 20),
        )

    def test_exam_list_page_loads(self):
        response = self.client.get(
            reverse("exams:exam_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mid Term")

    def test_exam_create_page_loads(self):
        response = self.client.get(
            reverse("exams:exam_create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Examination")

    def test_exam_detail_page_loads(self):
        response = self.client.get(
            reverse(
                "exams:exam_detail",
                kwargs={"pk": self.exam.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mid Term")
