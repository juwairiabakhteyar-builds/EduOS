from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Guardian
from .forms import GuardianForm


def guardian_list(request):

    guardians = Guardian.objects.all()

    return render(
        request,
        "guardians/guardian_list.html",
        {
            "guardians": guardians,
        },
    )


def guardian_create(request):

    if request.method == "POST":

        form = GuardianForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Guardian added successfully."
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
                "Guardian updated successfully."
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
            "Guardian deleted successfully."
        )

        return redirect("guardian_list")

    return render(
        request,
        "guardians/guardian_delete.html",
        {
            "guardian": guardian,
        },
    )