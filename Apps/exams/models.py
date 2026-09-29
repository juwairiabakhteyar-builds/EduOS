from django.core.exceptions import ValidationError
from django.db import models

from Apps.academics.models import AcademicLevel, AcademicSession, Section


class Exam(models.Model):
    name = models.CharField(max_length=100)
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    academic_level = models.ForeignKey(
        AcademicLevel,
        on_delete=models.PROTECT,
        related_name="exams",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "academic_session", "academic_level"],
                name="unique_exam_per_session_level",
            )
        ]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

    def __str__(self):
        return f"{self.name} - {self.academic_level} - {self.academic_session}"


class ExamSubject(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name = models.CharField(max_length=100)
    exam_date = models.DateField()
    max_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=33)

    class Meta:
        ordering = ["exam_date", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "name"],
                name="unique_subject_per_exam",
            )
        ]

    def clean(self):
        if self.passing_marks > self.max_marks:
            raise ValidationError(
                {"passing_marks": "Passing marks cannot exceed maximum marks."}
            )

        if not self.exam.start_date <= self.exam_date <= self.exam.end_date:
            raise ValidationError(
                {"exam_date": "Subject date must fall within the exam dates."}
            )

    def __str__(self):
        return f"{self.exam.name} - {self.name}"


class ExamResult(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="exam_results",
    )
    subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="results",
    )
    marks_obtained = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["student__first_name", "subject__exam_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject"],
                name="unique_result_per_student_subject",
            )
        ]

    def clean(self):
        if self.marks_obtained < 0:
            raise ValidationError(
                {"marks_obtained": "Marks cannot be negative."}
            )

        if self.subject_id and self.marks_obtained > self.subject.max_marks:
            raise ValidationError(
                {"marks_obtained": "Marks cannot exceed maximum marks."}
            )

    @property
    def is_passed(self):
        return self.marks_obtained >= self.subject.passing_marks

    def __str__(self):
        return f"{self.student} - {self.subject}"