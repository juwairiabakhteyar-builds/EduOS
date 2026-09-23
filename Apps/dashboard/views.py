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

    current_hour = timezone.localtime().hour

    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

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

    today_half_day = today_attendance.filter(
        status="Half Day"
    ).count()

    today_leave = today_attendance.filter(
        status="Leave"
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

    weekly_total = 0
    weekly_present = 0

    for i in range(7):

        current_date = week_start + timedelta(days=i)

        records = Attendance.objects.filter(
            attendance_date=current_date
        )

        total = records.count()

        present = records.filter(
            status="Present"
        ).count()

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

    # ------------------------------------------------------
    # RECENT STUDENT ADMISSIONS
    # ------------------------------------------------------

    recent_students = Student.objects.order_by(
        "-created_at"
    )[:5]

    # ------------------------------------------------------
    # RECENT ATTENDANCE
    # ------------------------------------------------------

    recent_attendance = Attendance.objects.select_related(
        "student"
    ).order_by(
        "-created_at"
    )[:5]

    # ------------------------------------------------------
    # UNIFIED ACTIVITY FEED
    # ------------------------------------------------------

    activities = []

    for student in recent_students:

        activities.append(
            {
                "type": "student",
                "title": "New student admission",
                "description": student.full_name,
                "time": student.created_at,
                "sort_time": student.created_at,
            }
        )

    for attendance in recent_attendance:

        activities.append(
            {
                "type": "attendance",
                "title": "Attendance marked",
                "description": (
                    f"{attendance.student.full_name} — "
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
        "today": today,
        "greeting": greeting,

        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_sections": total_sections,

        # Today
        "today_total": today_total,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_late": today_late,
        "today_half_day": today_half_day,
        "today_leave": today_leave,
        "attendance_percentage": attendance_percentage,

        # Weekly
        "weekly_attendance": weekly_attendance,
        "weekly_attendance_percentage": weekly_attendance_percentage,

        # Activity
        "recent_students": recent_students,
        "recent_attendance": recent_attendance,
        "activities": activities,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )