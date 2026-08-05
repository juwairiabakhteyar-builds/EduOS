from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Attendance


@login_required
def attendance_dashboard(request):

    total_records = Attendance.objects.count()

    present_count = Attendance.objects.filter(
        status="Present"
    ).count()

    absent_count = Attendance.objects.filter(
        status="Absent"
    ).count()

    late_count = Attendance.objects.filter(
        status="Late"
    ).count()

    leave_count = Attendance.objects.filter(
        status="Leave"
    ).count()

    context = {
        "total_records": total_records,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "leave_count": leave_count,
    }

    return render(
        request,
        "attendance/dashboard.html",
        context,
    )


@login_required
def mark_attendance(request):

    return render(
        request,
        "attendance/mark_attendance.html",
    )


@login_required
def attendance_records(request):

    records = (
        Attendance.objects
        .select_related(
            "person",
            "marked_by",
        )
        .order_by("-attendance_date")
    )

    return render(
        request,
        "attendance/attendance_records.html",
        {
            "records": records,
        },
    )


@login_required
def attendance_detail(request, pk):

    attendance = Attendance.objects.get(
        pk=pk,
    )

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance,
        },
    )