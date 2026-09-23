from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AcademicLevelForm, AcademicSessionForm, SectionForm
from .models import AcademicLevel, AcademicSession, Section


@login_required
def academics_dashboard(request):
    sessions = AcademicSession.objects.order_by("-name")
    levels = AcademicLevel.objects.annotate(
        student_count=Count("student", distinct=True)
    ).order_by("id")
    sections = Section.objects.annotate(
        student_count=Count("student", distinct=True)
    ).order_by("name")

    active_session = sessions.filter(is_active=True).first()

    return render(
        request,
        "academics/dashboard.html",
        {
            "sessions": sessions,
            "levels": levels,
            "sections": sections,
            "active_session": active_session,
            "session_count": sessions.count(),
            "level_count": levels.count(),
            "section_count": sections.count(),
        },
    )


@login_required
def session_create(request):
    if request.method == "POST":
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            if session.is_active:
                AcademicSession.objects.exclude(pk=session.pk).update(is_active=False)
            session.save()
            messages.success(request, "Academic session added successfully.")
            return redirect("academics_dashboard")
    else:
        form = AcademicSessionForm()

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Add Academic Session",
        "subtitle": "Create a new academic year for the school.",
        "back_url": "academics_dashboard",
    })


@login_required
def session_update(request, pk):
    session = get_object_or_404(AcademicSession, pk=pk)
    if request.method == "POST":
        form = AcademicSessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            if session.is_active:
                AcademicSession.objects.exclude(pk=session.pk).update(is_active=False)
            session.save()
            messages.success(request, "Academic session updated successfully.")
            return redirect("academics_dashboard")
    else:
        form = AcademicSessionForm(instance=session)

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Edit Academic Session",
        "subtitle": "Update the academic session details.",
        "back_url": "academics_dashboard",
    })


@login_required
def session_delete(request, pk):
    session = get_object_or_404(AcademicSession, pk=pk)
    if request.method == "POST":
        try:
            session.delete()
        except ProtectedError:
            messages.error(request, "This academic session cannot be deleted because students or other records are using it.")
            return redirect("academics_dashboard")
        messages.success(request, "Academic session deleted successfully.")
        return redirect("academics_dashboard")

    return render(request, "academics/delete.html", {
        "object": session,
        "object_type": "academic session",
        "back_url": "academics_dashboard",
    })


@login_required
def level_create(request):
    if request.method == "POST":
        form = AcademicLevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Academic level added successfully.")
            return redirect("academics_dashboard")
    else:
        form = AcademicLevelForm()

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Add Academic Level",
        "subtitle": "Add a class or early-years level to the school.",
        "back_url": "academics_dashboard",
    })


@login_required
def level_update(request, pk):
    level = get_object_or_404(AcademicLevel, pk=pk)
    if request.method == "POST":
        form = AcademicLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Academic level updated successfully.")
            return redirect("academics_dashboard")
    else:
        form = AcademicLevelForm(instance=level)

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Edit Academic Level",
        "subtitle": "Update the academic level name.",
        "back_url": "academics_dashboard",
    })


@login_required
def level_delete(request, pk):
    level = get_object_or_404(AcademicLevel, pk=pk)
    if request.method == "POST":
        try:
            level.delete()
        except ProtectedError:
            messages.error(request, "This academic level cannot be deleted because students are using it.")
            return redirect("academics_dashboard")
        messages.success(request, "Academic level deleted successfully.")
        return redirect("academics_dashboard")

    return render(request, "academics/delete.html", {
        "object": level,
        "object_type": "academic level",
        "back_url": "academics_dashboard",
    })


@login_required
def section_create(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Section added successfully.")
            return redirect("academics_dashboard")
    else:
        form = SectionForm()

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Add Section",
        "subtitle": "Create a section such as A, B or C.",
        "back_url": "academics_dashboard",
    })


@login_required
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully.")
            return redirect("academics_dashboard")
    else:
        form = SectionForm(instance=section)

    return render(request, "academics/form.html", {
        "form": form,
        "title": "Edit Section",
        "subtitle": "Update the section name.",
        "back_url": "academics_dashboard",
    })


@login_required
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        try:
            section.delete()
        except ProtectedError:
            messages.error(request, "This section cannot be deleted because students are using it.")
            return redirect("academics_dashboard")
        messages.success(request, "Section deleted successfully.")
        return redirect("academics_dashboard")

    return render(request, "academics/delete.html", {
        "object": section,
        "object_type": "section",
        "back_url": "academics_dashboard",
    })
