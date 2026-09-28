from datetime import date, timedelta

from django.test import TestCase

from Apps.academics.models import AcademicLevel, AcademicSession, Section
from Apps.students.models import Student

from .forms import StudentTransportForm
from .models import (
    RouteStop,
    StudentTransport,
    TransportAttendance,
    TransportRoute,
    Vehicle,
)


class TransportationModelTests(TestCase):
    def setUp(self):
        self.route = TransportRoute.objects.create(
            name="Route A",
            fare="1500.00",
        )

        self.stop = RouteStop.objects.create(
            route=self.route,
            name="Main Gate",
            stop_order=1,
        )

        self.vehicle = Vehicle.objects.create(
            name="EduOS Bus 1",
            registration_number="BR01AB1234",
            vehicle_type="bus",
            capacity=40,
        )

        self.academic_level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.academic_session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.section = Section.objects.create(
            name="A",
        )

    def create_student(self, first_name="Test", last_name="Student"):
        return Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date(2012, 1, 1),
            academic_level=self.academic_level,
            academic_session=self.academic_session,
            section=self.section,
        )

    def test_vehicle_string(self):
        self.assertEqual(
            str(self.vehicle),
            "EduOS Bus 1 - BR01AB1234",
        )

    def test_route_string(self):
        self.assertEqual(
            str(self.route),
            "Route A",
        )

    def test_route_stop_string(self):
        self.assertEqual(
            str(self.stop),
            "Route A - Main Gate",
        )

    def test_student_transport_assignment(self):
        student = self.create_student()

        assignment = StudentTransport.objects.create(
            student=student,
            route=self.route,
            pickup_stop=self.stop,
            vehicle=self.vehicle,
            start_date=date.today(),
        )

        self.assertEqual(assignment.route, self.route)
        self.assertEqual(assignment.pickup_stop, self.stop)
        self.assertEqual(assignment.vehicle, self.vehicle)
        self.assertTrue(assignment.is_active)

    def test_attendance_record(self):
        student = self.create_student(
            first_name="Attendance",
        )

        assignment = StudentTransport.objects.create(
            student=student,
            route=self.route,
            pickup_stop=self.stop,
            start_date=date.today(),
        )

        attendance = TransportAttendance.objects.create(
            assignment=assignment,
            date=date.today(),
            status="present",
        )

        self.assertEqual(attendance.status, "present")
        self.assertEqual(attendance.assignment, assignment)


class TransportationFormTests(TestCase):
    def setUp(self):
        self.route = TransportRoute.objects.create(
            name="Route B",
            fare="1200.00",
        )

        self.other_route = TransportRoute.objects.create(
            name="Route C",
            fare="1300.00",
        )

        self.stop = RouteStop.objects.create(
            route=self.route,
            name="School Road",
            stop_order=1,
        )

        self.other_stop = RouteStop.objects.create(
            route=self.other_route,
            name="Market Road",
            stop_order=1,
        )

        self.vehicle = Vehicle.objects.create(
            name="Van 1",
            registration_number="BR02CD5678",
            vehicle_type="van",
            capacity=15,
        )

        self.academic_level = AcademicLevel.objects.create(
            name="Class 10",
        )

        self.academic_session = AcademicSession.objects.create(
            name="2026-2027",
            is_active=True,
        )

        self.section = Section.objects.create(
            name="A",
        )

        self.student = Student.objects.create(
            first_name="Form",
            last_name="Student",
            date_of_birth=date(2012, 1, 1),
            academic_level=self.academic_level,
            academic_session=self.academic_session,
            section=self.section,
        )

    def test_inactive_route_is_not_available(self):
        self.route.is_active = False
        self.route.save(update_fields=["is_active"])

        form = StudentTransportForm()

        self.assertNotIn(
            self.route,
            form.fields["route"].queryset,
        )

        self.assertIn(
            self.other_route,
            form.fields["route"].queryset,
        )

    def test_inactive_vehicle_is_not_available(self):
        self.vehicle.is_active = False
        self.vehicle.save(update_fields=["is_active"])

        form = StudentTransportForm()

        self.assertNotIn(
            self.vehicle,
            form.fields["vehicle"].queryset,
        )

    def test_student_transport_form_accepts_matching_stop(self):
        form = StudentTransportForm(
            data={
                "student": self.student.pk,
                "route": self.route.pk,
                "pickup_stop": self.stop.pk,
                "vehicle": self.vehicle.pk,
                "start_date": date.today(),
                "end_date": "",
                "is_active": "on",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_student_transport_form_rejects_wrong_route_stop(self):
        form = StudentTransportForm(
            data={
                "student": self.student.pk,
                "route": self.route.pk,
                "pickup_stop": self.other_stop.pk,
                "vehicle": self.vehicle.pk,
                "start_date": date.today(),
                "end_date": "",
                "is_active": "on",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "pickup_stop",
            form.errors,
        )

    def test_student_transport_form_rejects_invalid_date_range(self):
        start_date = date.today()
        end_date = start_date - timedelta(days=1)

        form = StudentTransportForm(
            data={
                "student": self.student.pk,
                "route": self.route.pk,
                "pickup_stop": self.stop.pk,
                "vehicle": self.vehicle.pk,
                "start_date": start_date,
                "end_date": end_date,
                "is_active": "on",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "end_date",
            form.errors,
        )
