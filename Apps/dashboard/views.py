from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from Apps.students.models import Student
from Apps.teachers.models import Teacher
from Apps.academics.models import AcademicLevel, Section
from Apps.attendance.models import Attendance


@login_required
def dashboard(request):

    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    # ------------------------------------------------------
    # BASIC COUNTS
    # ------------------------------------------------------

    total_students = Student.objects.count()

    total_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    total_classes = AcademicLevel.objects.count()

    total_sections = Section.objects.count()

    # ------------------------------------------------------
    # TODAY'S ATTENDANCE
    # ------------------------------------------------------

    today_attendance = Attendance.objects.filter(
        attendance_date=today
    )

    today_total = today_attendance.count()

    today_present = today_attendance.filter(
        status="Present"
    ).count()

    today_absent = today_attendance.filter(
        status="Absent"
    ).count()

    today_late = today_attendance.filter(
        status="Late"
    ).count()

    if today_total:
        attendance_percentage = round(
            (today_present / today_total) * 100,
            1,
        )
    else:
        attendance_percentage = 0

    # ------------------------------------------------------
    # WEEKLY ATTENDANCE
    # ------------------------------------------------------

    weekly_attendance = []

    for i in range(7):

        current_date = week_start + timedelta(days=i)

        records = Attendance.objects.filter(
            attendance_date=current_date
        )

        total = records.count()

        present = records.filter(
            status="Present"
        ).count()

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

    # ------------------------------------------------------
    # RECENT STUDENT ADMISSIONS
    # ------------------------------------------------------

    recent_students = Student.objects.order_by(
        "-id"
    )[:5]

    # ------------------------------------------------------
    # RECENT ATTENDANCE ACTIVITY
    # ------------------------------------------------------

    recent_attendance = Attendance.objects.select_related(
        "student"
    ).order_by(
        "-created_at"
    )[:5]

    # ------------------------------------------------------
    # UNIFIED RECENT ACTIVITY FEED
    # ------------------------------------------------------

    activities = []

    for student in recent_students:

        activities.append(
            {
                "type": "student",
                "icon": "🎓",
                "title": "New student admission",
                "description": (
                    f"{student.first_name} "
                    f"{student.last_name}"
                ),
                "time": student.created_at,
                "sort_time": student.created_at,
            }
        )

    for attendance in recent_attendance:

        activities.append(
            {
                "type": "attendance",
                "icon": "✓",
                "title": "Attendance marked",
                "description": (
                    f"{attendance.student.first_name} "
                    f"{attendance.student.last_name} — "
                    f"{attendance.status}"
                ),
                "time": attendance.created_at,
                "sort_time": attendance.created_at,
            }
        )

    activities.sort(
        key=lambda item: item["sort_time"],
        reverse=True,
    )

    activities = activities[:8]

    # ------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------

    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_sections": total_sections,

        "today": today,

        "today_total": today_total,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_late": today_late,
        "attendance_percentage": attendance_percentage,

        "weekly_attendance": weekly_attendance,

        "activities": activities,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )