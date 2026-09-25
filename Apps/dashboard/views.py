from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from Apps.academics.models import AcademicLevel, Section
from Apps.attendance.models import Attendance
from Apps.students.models import Student
from Apps.teachers.models import Teacher

from .models import ActivityLog


@login_required
def dashboard(request):

    today = timezone.localdate()

    current_hour = timezone.localtime().hour

    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    week_start = today - timedelta(days=6)

    # --------------------------------------------------
    # BASIC COUNTS
    # --------------------------------------------------

    total_students = Student.objects.count()

    total_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    total_classes = AcademicLevel.objects.count()

    total_sections = Section.objects.count()

    # --------------------------------------------------
    # TODAY'S ATTENDANCE
    # --------------------------------------------------

    today_attendance = Attendance.objects.filter(
        attendance_date=today
    )

    today_summary = today_attendance.aggregate(
        total=Count("id"),
        present=Count(
            "id",
            filter=Q(status="Present"),
        ),
        absent=Count(
            "id",
            filter=Q(status="Absent"),
        ),
        late=Count(
            "id",
            filter=Q(status="Late"),
        ),
        half_day=Count(
            "id",
            filter=Q(status="Half Day"),
        ),
        leave=Count(
            "id",
            filter=Q(status="Leave"),
        ),
    )

    today_total = today_summary["total"] or 0
    today_present = today_summary["present"] or 0
    today_absent = today_summary["absent"] or 0
    today_late = today_summary["late"] or 0
    today_half_day = today_summary["half_day"] or 0
    today_leave = today_summary["leave"] or 0

    if today_total:
        attendance_percentage = round(
            (today_present / today_total) * 100,
            1,
        )
    else:
        attendance_percentage = 0

    # --------------------------------------------------
    # WEEKLY ATTENDANCE
    # --------------------------------------------------

    weekly_records = (
        Attendance.objects
        .filter(
            attendance_date__range=[
                week_start,
                today,
            ]
        )
        .values("attendance_date")
        .annotate(
            total=Count("id"),
            present=Count(
                "id",
                filter=Q(status="Present"),
            ),
        )
    )

    weekly_lookup = {
        record["attendance_date"]: record
        for record in weekly_records
    }

    weekly_attendance = []

    weekly_total = 0
    weekly_present = 0

    for i in range(7):

        current_date = week_start + timedelta(days=i)

        record = weekly_lookup.get(
            current_date,
            {
                "total": 0,
                "present": 0,
            },
        )

        total = record["total"]
        present = record["present"]

        weekly_total += total
        weekly_present += present

        if total:
            percentage = round(
                (present / total) * 100,
                1,
            )
        else:
            percentage = 0

        weekly_attendance.append(
            {
                "date": current_date,
                "day": current_date.strftime("%a"),
                "percentage": percentage,
                "total": total,
                "present": present,
            }
        )

    if weekly_total:
        weekly_attendance_percentage = round(
            (weekly_present / weekly_total) * 100,
            1,
        )
    else:
        weekly_attendance_percentage = 0

    # --------------------------------------------------
    # RECENT STUDENT ADMISSIONS
    # --------------------------------------------------

    recent_students = (
        Student.objects
        .select_related(
            "academic_level",
            "section",
        )
        .order_by("-created_at")[:5]
    )

    # --------------------------------------------------
    # RECENT ATTENDANCE
    # --------------------------------------------------

    recent_attendance = (
        Attendance.objects
        .select_related("student")
        .order_by("-created_at")[:5]
    )

    # --------------------------------------------------
    # ACTIVITY FEED
    # --------------------------------------------------

    activities = ActivityLog.objects.select_related(
        "actor"
    ).order_by("-created_at")[:8]

    context = {
        "today": today,
        "greeting": greeting,

        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_sections": total_sections,

        "today_total": today_total,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_late": today_late,
        "today_half_day": today_half_day,
        "today_leave": today_leave,
        "attendance_percentage": attendance_percentage,

        "weekly_attendance": weekly_attendance,
        "weekly_attendance_percentage": (
            weekly_attendance_percentage
        ),

        "recent_students": recent_students,
        "recent_attendance": recent_attendance,
        "activities": activities,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )