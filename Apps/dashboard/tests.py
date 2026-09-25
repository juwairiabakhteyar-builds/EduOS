from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.attendance.models import Attendance
from Apps.guardians.models import Guardian
from Apps.students.models import Student
from Apps.teachers.models import Teacher

from Apps.dashboard.models import ActivityLog
from Apps.dashboard.utils import log_activity


class DashboardViewTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="dashboardtest",
            password="testpassword123",
            role="school_admin",
        )

        self.session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.section = Section.objects.create(
            name="A",
        )

        self.guardian = Guardian.objects.create(
            first_name="Test",
            last_name="Guardian",
            relationship="Father",
            mobile_number="9000000010",
            email="guardian@example.com",
        )

    def login(self):
        self.client.login(
            username="dashboardtest",
            password="testpassword123",
        )

    def create_student(
        self,
        first_name="Test",
        last_name="Student",
    ):
        return Student.objects.create(
            first_name=first_name,
            middle_name="",
            last_name=last_name,
            gender="Female",
            date_of_birth=date(2012, 1, 1),
            academic_session=self.session,
            academic_level=self.level,
            section=self.section,
            guardian=self.guardian,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/dashboard.html",
        )

    def test_dashboard_counts_active_teachers(self):
        Teacher.objects.create(
            first_name="Active",
            middle_name="",
            last_name="Teacher",
            gender="Female",
            date_of_birth=date(1995, 1, 1),
            mobile_number="9000000001",
            email="active.teacher@example.com",
            qualification="B.Ed",
            experience=5,
            joining_date=date(2020, 1, 1),
            designation="Teacher",
            status="Active",
        )

        Teacher.objects.create(
            first_name="Inactive",
            middle_name="",
            last_name="Teacher",
            gender="Male",
            date_of_birth=date(1990, 1, 1),
            mobile_number="9000000002",
            email="inactive.teacher@example.com",
            qualification="B.Ed",
            experience=8,
            joining_date=date(2018, 1, 1),
            designation="Teacher",
            status="Inactive",
        )

        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["total_teachers"],
            1,
        )

    def test_dashboard_empty_attendance(self):
        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["today_total"], 0)
        self.assertEqual(response.context["today_present"], 0)
        self.assertEqual(response.context["today_absent"], 0)
        self.assertEqual(response.context["attendance_percentage"], 0)
        self.assertEqual(
            response.context["weekly_attendance_percentage"],
            0,
        )

    def test_dashboard_student_count(self):
        self.create_student(
            first_name="Aisha",
            last_name="Khan",
        )
        self.create_student(
            first_name="Sara",
            last_name="Ali",
        )

        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["total_students"],
            2,
        )

    def test_dashboard_attendance_counts(self):
        student_one = self.create_student(
            first_name="Aisha",
            last_name="Khan",
        )

        student_two = self.create_student(
            first_name="Sara",
            last_name="Ali",
        )

        today = timezone.localdate()

        Attendance.objects.create(
            student=student_one,
            attendance_date=today,
            status="Present",
            marked_by=self.user,
        )

        Attendance.objects.create(
            student=student_two,
            attendance_date=today,
            status="Absent",
            marked_by=self.user,
        )

        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["today_total"], 2)
        self.assertEqual(response.context["today_present"], 1)
        self.assertEqual(response.context["today_absent"], 1)
        self.assertEqual(response.context["attendance_percentage"], 50.0)

    def test_dashboard_recent_students(self):
        student = self.create_student(
            first_name="Aisha",
            last_name="Khan",
        )

        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)

        recent_students = list(
            response.context["recent_students"]
        )

        self.assertIn(student, recent_students)

    def test_dashboard_recent_attendance(self):
        student = self.create_student(
            first_name="Aisha",
            last_name="Khan",
        )

        today = timezone.localdate()

        attendance = Attendance.objects.create(
            student=student,
            attendance_date=today,
            status="Present",
            marked_by=self.user,
        )

        self.login()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)

        recent_attendance = list(
            response.context["recent_attendance"]
        )

        self.assertIn(attendance, recent_attendance)

    def test_activity_log_created(self):
        student = self.create_student(
            first_name="Audit",
            last_name="Student",
        )

        log_activity(
            actor=self.user,
            instance=student,
            module="Students",
            action="created",
            description=f"New student admitted: {student.full_name}",
        )

        activity = ActivityLog.objects.get()

        self.assertEqual(
            activity.actor,
            self.user,
        )

        self.assertEqual(
            activity.module,
            "Students",
        )

        self.assertEqual(
            activity.action,
            "created",
        )

        self.assertEqual(
            activity.description,
            f"New student admitted: {student.full_name}",
        )

        self.assertEqual(
            activity.content_object,
            student,
        )


    def test_activity_log_updated(self):
        student = self.create_student(
            first_name="Audit",
            last_name="Student",
        )

        log_activity(
            actor=self.user,
            instance=student,
            module="Students",
            action="updated",
            description=f"Student updated: {student.full_name}",
        )

        activity = ActivityLog.objects.get()

        self.assertEqual(
            activity.actor,
            self.user,
        )

        self.assertEqual(
            activity.action,
            "updated",
        )

        self.assertEqual(
            activity.content_object,
            student,
        )


    def test_activity_log_deleted(self):
        student = self.create_student(
            first_name="Audit",
            last_name="Student",
        )

        log_activity(
            actor=self.user,
            instance=student,
            module="Students",
            action="deleted",
            description=f"Student deleted: {student.full_name}",
        )

        activity = ActivityLog.objects.get()

        self.assertEqual(
            activity.actor,
            self.user,
        )

        self.assertEqual(
            activity.action,
            "deleted",
        )

        self.assertEqual(
            activity.content_object,
            student,
        )


    def test_activity_log_without_actor(self):
        student = self.create_student(
            first_name="System",
            last_name="Event",
        )

        log_activity(
            actor=None,
            instance=student,
            module="Students",
            action="created",
            description="System-created student record",
        )

        activity = ActivityLog.objects.get()

        self.assertIsNone(
            activity.actor,
        )

        self.assertEqual(
            activity.action,
            "created",
        )

        self.assertEqual(
            activity.content_object,
            student,
        )
