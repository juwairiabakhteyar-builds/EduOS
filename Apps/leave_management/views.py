from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .models import LeaveType
from .forms import LeaveTypeForm


def leave_type_list(request):

    query = request.GET.get("q")

    leave_types = LeaveType.objects.all().order_by("leave_name")

    if query:

        leave_types = (
            leave_types.filter(leave_name__icontains=query)
            | leave_types.filter(leave_code__icontains=query)
        )

    paginator = Paginator(
        leave_types,
        10,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "leave_management/leave_type_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        },
    )


def leave_type_create(request):

    if request.method == "POST":

        form = LeaveTypeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Leave Type added successfully."
            )

            return redirect(
                "leave_type_list"
            )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = LeaveTypeForm()

    return render(
        request,
        "leave_management/leave_type_form.html",
        {
            "form": form,
        },
    )


def leave_type_detail(request, pk):

    leave_type = get_object_or_404(
        LeaveType,
        pk=pk,
    )

    return render(
        request,
        "leave_management/leave_type_detail.html",
        {
            "leave_type": leave_type,
        },
    )


def leave_type_update(request, pk):

    leave_type = get_object_or_404(
        LeaveType,
        pk=pk,
    )

    if request.method == "POST":

        form = LeaveTypeForm(
            request.POST,
            instance=leave_type,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Leave Type updated successfully."
            )

            return redirect(
                "leave_type_detail",
                pk=leave_type.pk,
            )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = LeaveTypeForm(
            instance=leave_type,
        )

    return render(
        request,
        "leave_management/leave_type_form.html",
        {
            "form": form,
            "leave_type": leave_type,
        },
    )


def leave_type_delete(request, pk):

    leave_type = get_object_or_404(
        LeaveType,
        pk=pk,
    )

    if request.method == "POST":

        leave_type.delete()

        messages.success(
            request,
            "Leave Type deleted successfully."
        )

        return redirect(
            "leave_type_list"
        )

    return render(
        request,
        "leave_management/leave_type_delete.html",
        {
            "leave_type": leave_type,
        },
    )