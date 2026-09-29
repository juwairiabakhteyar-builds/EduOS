from django.contrib import admin

from .models import Exam, ExamResult, ExamSubject


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "academic_session",
        "academic_level",
        "start_date",
        "end_date",
        "is_published",
    )
    list_filter = (
        "academic_session",
        "academic_level",
        "is_published",
    )
    search_fields = (
        "name",
        "academic_session__name",
        "academic_level__name",
    )


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "exam",
        "exam_date",
        "max_marks",
        "passing_marks",
    )
    list_filter = ("exam", "exam_date")
    search_fields = (
        "name",
        "exam__name",
    )


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "marks_obtained",
        "remarks",
    )
    list_filter = (
        "subject__exam",
        "subject",
    )
    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__student_id",
        "student__admission_number",
        "subject__name",
    )
