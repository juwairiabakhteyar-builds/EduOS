from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Attendance
from .forms import AttendanceFilterForm

from Apps.students.models import Student

from Apps.dashboard.utils import log_activity

from Apps.academics.models import (
    AcademicSession,
    AcademicLevel,
    Section,
)


# ============================================================
# ATTENDANCE DASHBOARD
# ============================================================

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

    half_day_count = Attendance.objects.filter(
        status="Half Day"
    ).count()

    leave_count = Attendance.objects.filter(
        status="Leave"
    ).count()

    recent_records = (
        Attendance.objects
        .select_related(
            "student",
            "academic_session",
            "academic_level",
            "section",
            "marked_by",
        )
        .order_by("-created_at")[:5]
    )

    context = {
        "total_records": total_records,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "half_day_count": half_day_count,
        "leave_count": leave_count,
        "recent_records": recent_records,
    }

    return render(
        request,
        "attendance/dashboard.html",
        context,
    )


# ============================================================
# MARK ATTENDANCE
# ============================================================

@login_required
def mark_attendance(request):

    # --------------------------------------------------------
    # SAVE ATTENDANCE
    # --------------------------------------------------------

    if request.method == "POST":

        academic_session_id = request.POST.get(
            "academic_session"
        )

        academic_level_id = request.POST.get(
            "academic_level"
        )

        section_id = request.POST.get(
            "section"
        )

        attendance_date = request.POST.get(
            "attendance_date"
        )

        academic_session = get_object_or_404(
            AcademicSession,
            pk=academic_session_id,
        )

        academic_level = get_object_or_404(
            AcademicLevel,
            pk=academic_level_id,
        )

        section = get_object_or_404(
            Section,
            pk=section_id,
        )

        students = (
            Student.objects
            .filter(
                academic_session=academic_session,
                academic_level=academic_level,
                section=section,
            )
            .order_by(
                "first_name",
                "last_name",
            )
        )

        for student in students:

            status = request.POST.get(
                f"status_{student.id}"
            )

            if status:

                attendance, created = Attendance.objects.update_or_create(
                    student=student,
                    attendance_date=attendance_date,
                    defaults={
                        "academic_session": academic_session,
                        "academic_level": academic_level,
                        "section": section,
                        "status": status,
                        "marked_by": request.user,
                    },
                )

                if created:

                    log_activity(
                        actor=request.user,
                        instance=attendance,
                        module="Attendance",
                        action="created",
                        description=(
                            f"Attendance marked for "
                            f"{student.full_name}: {status}"
                        ),
                    )

                else:

                    log_activity(
                        actor=request.user,
                        instance=attendance,
                        module="Attendance",
                        action="updated",
                        description=(
                            f"Attendance updated for "
                            f"{student.full_name}: {status}"
                        ),
                    )

        return redirect("attendance_records")

    # --------------------------------------------------------
    # LOAD STUDENTS
    # --------------------------------------------------------

    form = AttendanceFilterForm()

    students = Student.objects.none()

    selected_session = None
    selected_level = None
    selected_section = None
    selected_date = None

    if request.GET:

        form = AttendanceFilterForm(
            request.GET
        )

        if form.is_valid():

            academic_session = (
                form.cleaned_data[
                    "academic_session"
                ]
            )

            academic_level = (
                form.cleaned_data[
                    "academic_level"
                ]
            )

            section = (
                form.cleaned_data[
                    "section"
                ]
            )

            selected_date = (
                form.cleaned_data[
                    "attendance_date"
                ]
            )

            selected_session = academic_session.pk
            selected_level = academic_level.pk
            selected_section = section.pk

            students = (
                Student.objects
                .filter(
                    academic_session=academic_session,
                    academic_level=academic_level,
                    section=section,
                )
                .order_by(
                    "first_name",
                    "last_name",
                )
            )

    context = {
        "form": form,
        "students": students,
        "selected_session": selected_session,
        "selected_level": selected_level,
        "selected_section": selected_section,
        "selected_date": selected_date,
    }

    return render(
        request,
        "attendance/mark_attendance.html",
        context,
    )


# ============================================================
# ATTENDANCE RECORDS
# ============================================================

@login_required
def attendance_records(request):

    records = (
        Attendance.objects
        .select_related(
            "student",
            "academic_session",
            "academic_level",
            "section",
            "marked_by",
        )
        .order_by(
            "-attendance_date",
            "student__first_name",
            "student__last_name",
        )
    )

    # --------------------------------------------------------
    # FILTER VALUES
    # --------------------------------------------------------

    academic_session = request.GET.get(
        "academic_session"
    )

    academic_level = request.GET.get(
        "academic_level"
    )

    section = request.GET.get(
        "section"
    )

    status = request.GET.get(
        "status"
    )

    from_date = request.GET.get(
    "from_date"
    )

    to_date = request.GET.get(
    "to_date"
    )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    if academic_session:

        records = records.filter(
            academic_session_id=academic_session
        )

    if academic_level:

        records = records.filter(
            academic_level_id=academic_level
        )

    if section:

        records = records.filter(
            section_id=section
        )

    if status:

        records = records.filter(
            status=status
        )

    if from_date:

        records = records.filter(
            attendance_date__gte=from_date
        )

    if to_date:

        records = records.filter(
            attendance_date__lte=to_date
        )

    context = {
        "records": records,

        "academic_sessions":
            AcademicSession.objects.all(),

        "academic_levels":
            AcademicLevel.objects.all(),

        "sections":
            Section.objects.all(),

        "status_choices":
            Attendance.STATUS_CHOICES,

        "selected_session":
            academic_session,

        "selected_level":
            academic_level,

        "selected_section":
            section,

        "selected_status":
            status,

        "selected_from_date":
            from_date,

        "selected_to_date":
            to_date,
    }

    return render(
        request,
        "attendance/attendance_records.html",
        context,
    )


# ============================================================
# ATTENDANCE DETAIL
# ============================================================

@login_required
def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance,
        },
    )

# ============================================================
# EDIT ATTENDANCE
# ============================================================

@login_required
def attendance_edit(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        attendance.status = request.POST.get("status")

        attendance.remarks = request.POST.get(
            "remarks",
            "",
        )

        attendance.marked_by = request.user

        attendance.save()

        log_activity(
            actor=request.user,
            instance=attendance,
            module="Attendance",
            action="updated",
            description=(
                f"Attendance updated for "
                f"{attendance.student.full_name}: "
                f"{attendance.status}"
            ),
        )

        return redirect(
            "attendance_detail",
            pk=attendance.pk,
        )

    return render(
        request,
        "attendance/attendance_edit.html",
        {
            "attendance": attendance,
        },
    )

# ============================================================
# DELETE ATTENDANCE
# ============================================================

@login_required
def attendance_delete(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        student_name = attendance.student.full_name
        attendance_date = attendance.attendance_date
        attendance_status = attendance.status

        log_activity(
            actor=request.user,
            instance=attendance,
            module="Attendance",
            action="deleted",
            description=(
                f"Attendance deleted for "
                f"{student_name} on "
                f"{attendance_date}: "
                f"{attendance_status}"
            ),
        )

        attendance.delete()

        return redirect(
            "attendance_records"
        )

    return render(
        request,
        "attendance/attendance_delete.html",
        {
            "attendance": attendance,
        },
    )