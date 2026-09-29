from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExamForm, ExamResultForm, ExamSubjectForm
from .models import Exam, ExamResult, ExamSubject


def exam_list(request):
    exams = (
        Exam.objects.select_related(
            "academic_session",
            "academic_level",
        )
        .annotate(subject_count=Count("subjects", distinct=True))
        .order_by("-start_date", "name")
    )

    return render(
        request,
        "exams/exam_list.html",
        {"exams": exams},
    )


def exam_create(request):
    if request.method == "POST":
        form = ExamForm(request.POST)

        if form.is_valid():
            exam = form.save()
            messages.success(
                request,
                f'Exam "{exam.name}" created successfully.',
            )
            return redirect("exams:exam_detail", pk=exam.pk)
    else:
        form = ExamForm()

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form,
            "page_title": "Create Exam",
        },
    )


def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)

        if form.is_valid():
            exam = form.save()
            messages.success(
                request,
                f'Exam "{exam.name}" updated successfully.',
            )
            return redirect("exams:exam_detail", pk=exam.pk)
    else:
        form = ExamForm(instance=exam)

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form,
            "page_title": "Edit Exam",
            "exam": exam,
        },
    )


def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == "POST":
        exam_name = exam.name
        exam.delete()
        messages.success(
            request,
            f'Exam "{exam_name}" deleted successfully.',
        )
        return redirect("exams:exam_list")

    return render(
        request,
        "exams/exam_confirm_delete.html",
        {"exam": exam},
    )


def exam_detail(request, pk):
    exam = get_object_or_404(
        Exam.objects.select_related(
            "academic_session",
            "academic_level",
        ),
        pk=pk,
    )

    subjects = exam.subjects.all()

    results = (
        ExamResult.objects.filter(subject__exam=exam)
        .select_related("student", "subject")
        .order_by(
            "student__first_name",
            "student__last_name",
            "subject__exam_date",
        )
    )

    return render(
        request,
        "exams/exam_detail.html",
        {
            "exam": exam,
            "subjects": subjects,
            "results": results,
        },
    )


def subject_create(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)

    if request.method == "POST":
        form = ExamSubjectForm(request.POST)

        if form.is_valid():
            subject = form.save(commit=False)
            subject.exam = exam

            try:
                subject.full_clean()
                subject.save()
            except Exception as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(
                    request,
                    f'Subject "{subject.name}" added successfully.',
                )
                return redirect(
                    "exams:exam_detail",
                    pk=exam.pk,
                )
    else:
        form = ExamSubjectForm(
            initial={
                "exam_date": exam.start_date,
            }
        )

    return render(
        request,
        "exams/subject_form.html",
        {
            "form": form,
            "exam": exam,
            "page_title": "Add Exam Subject",
        },
    )


def result_create(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)

    if request.method == "POST":
        form = ExamResultForm(request.POST)

        if form.is_valid():
            result = form.save(commit=False)

            if result.subject.exam_id != exam.pk:
                form.add_error(
                    "subject",
                    "Selected subject does not belong to this exam.",
                )
            else:
                try:
                    result.full_clean()
                    result.save()
                except Exception as exc:
                    form.add_error(None, str(exc))
                else:
                    messages.success(
                        request,
                        "Exam result saved successfully.",
                    )
                    return redirect(
                        "exams:exam_detail",
                        pk=exam.pk,
                    )
    else:
        form = ExamResultForm()

    form.fields["subject"].queryset = ExamSubject.objects.filter(
        exam=exam
    ).order_by("exam_date", "name")

    return render(
        request,
        "exams/result_form.html",
        {
            "form": form,
            "exam": exam,
            "page_title": "Add Exam Result",
        },
    )
