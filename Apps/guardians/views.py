from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GuardianForm
from .models import Guardian


def guardian_list(request):
    query = request.GET.get("q", "").strip()
    relationship = request.GET.get("relationship", "").strip()

    guardians = Guardian.objects.all().order_by("first_name", "last_name")

    if query:
        guardians = guardians.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(mobile_number__icontains=query)
            | Q(email__icontains=query)
            | Q(occupation__icontains=query)
        )

    if relationship:
        guardians = guardians.filter(relationship=relationship)

    paginator = Paginator(guardians, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "guardians/guardian_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "relationship": relationship,
            "relationship_choices": Guardian.RELATIONSHIP_CHOICES,
        },
    )


def guardian_create(request):
    if request.method == "POST":
        form = GuardianForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Guardian added successfully.",
            )

            return redirect("guardian_list")
    else:
        form = GuardianForm()

    return render(
        request,
        "guardians/guardian_create.html",
        {
            "form": form,
        },
    )


def guardian_detail(request, pk):
    guardian = get_object_or_404(
        Guardian,
        pk=pk,
    )

    return render(
        request,
        "guardians/guardian_detail.html",
        {
            "guardian": guardian,
        },
    )


def guardian_update(request, pk):
    guardian = get_object_or_404(
        Guardian,
        pk=pk,
    )

    if request.method == "POST":
        form = GuardianForm(
            request.POST,
            instance=guardian,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Guardian updated successfully.",
            )

            return redirect(
                "guardian_detail",
                pk=guardian.pk,
            )
    else:
        form = GuardianForm(
            instance=guardian,
        )

    return render(
        request,
        "guardians/guardian_create.html",
        {
            "form": form,
            "guardian": guardian,
        },
    )


def guardian_delete(request, pk):
    guardian = get_object_or_404(
        Guardian,
        pk=pk,
    )

    if request.method == "POST":
        guardian.delete()

        messages.success(
            request,
            "Guardian deleted successfully.",
        )

        return redirect("guardian_list")

    return render(
        request,
        "guardians/guardian_delete.html",
        {
            "guardian": guardian,
        },
    )
