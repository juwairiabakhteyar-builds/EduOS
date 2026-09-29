from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import HomeworkAssignmentForm
from .models import HomeworkAssignment


@login_required
def homework_dashboard(request):
    assignments = HomeworkAssignment.objects.select_related(
        "teacher",
        "academic_session",
        "academic_level",
        "section",
    )

    context = {
        "total_assignments": assignments.count(),
        "published_assignments": assignments.filter(
            is_published=True
        ).count(),
        "draft_assignments": assignments.filter(
            is_published=False
        ).count(),
        "recent_assignments": assignments[:10],
    }

    return render(
        request,
        "homework/dashboard.html",
        context,
    )


@login_required
def assignment_list(request):
    query = request.GET.get("q", "").strip()

    assignments = HomeworkAssignment.objects.select_related(
        "teacher",
        "academic_session",
        "academic_level",
        "section",
    )

    if query:
        assignments = assignments.filter(
            Q(title__icontains=query)
            | Q(subject__icontains=query)
            | Q(description__icontains=query)
            | Q(teacher__first_name__icontains=query)
            | Q(teacher__last_name__icontains=query)
        )

    return render(
        request,
        "homework/assignment_list.html",
        {
            "assignments": assignments,
            "query": query,
        },
    )


@login_required
def assignment_create(request):
    if request.method == "POST":
        form = HomeworkAssignmentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Homework assignment created successfully.",
            )
            return redirect("homework:assignment_list")
    else:
        form = HomeworkAssignmentForm()

    return render(
        request,
        "homework/form.html",
        {
            "form": form,
            "title": "Create Homework Assignment",
            "cancel_url": "homework:assignment_list",
        },
    )


@login_required
def assignment_update(request, pk):
    assignment = get_object_or_404(
        HomeworkAssignment,
        pk=pk,
    )

    if request.method == "POST":
        form = HomeworkAssignmentForm(
            request.POST,
            request.FILES,
            instance=assignment,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Homework assignment updated successfully.",
            )
            return redirect("homework:assignment_list")
    else:
        form = HomeworkAssignmentForm(instance=assignment)

    return render(
        request,
        "homework/form.html",
        {
            "form": form,
            "title": "Edit Homework Assignment",
            "cancel_url": "homework:assignment_list",
        },
    )


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(
        HomeworkAssignment,
        pk=pk,
    )

    if request.method == "POST":
        assignment.delete()

        messages.success(
            request,
            "Homework assignment deleted successfully.",
        )

        return redirect("homework:assignment_list")

    return render(
        request,
        "homework/delete.html",
        {
            "object": assignment,
            "title": "Delete Homework Assignment",
            "cancel_url": "homework:assignment_list",
        },
    )