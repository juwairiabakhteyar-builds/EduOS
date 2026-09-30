from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import NotificationForm
from .models import Notification, NotificationRead


def can_manage_notifications(user):
    return user.is_superuser or user.role in {
        "super_admin",
        "school_admin",
        "principal",
    }


def visible_notifications(user):
    role_map = {
        "student": {"all", "students"},
        "parent": {"all", "parents"},
        "teacher": {"all", "teachers"},
        "staff": {"all", "staff"},
    }

    audiences = role_map.get(user.role, {"all", "staff"})

    queryset = Notification.objects.filter(
        published=True,
        audience__in=audiences,
    )

    if getattr(user, "school_id", None):
        queryset = queryset.filter(
            created_by__school_id=user.school_id
        )

    return queryset


@login_required
def notification_list(request):
    notifications = visible_notifications(request.user).annotate(
        is_read=Exists(
            NotificationRead.objects.filter(
                notification=OuterRef("pk"),
                user=request.user,
            )
        )
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "can_manage": can_manage_notifications(request.user),
        },
    )


@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(
        visible_notifications(request.user),
        pk=pk,
    )

    NotificationRead.objects.get_or_create(
        notification=notification,
        user=request.user,
    )

    return render(
        request,
        "notifications/notification_detail.html",
        {
            "notification": notification,
            "can_manage": can_manage_notifications(request.user),
        },
    )


@login_required
def notification_create(request):
    if not can_manage_notifications(request.user):
        return redirect("notifications:list")

    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.created_by = request.user
            notification.save()
            return redirect("notifications:detail", pk=notification.pk)
    else:
        form = NotificationForm()

    return render(
        request,
        "notifications/notification_form.html",
        {"form": form, "page_title": "Create Notification"},
    )


@login_required
def notification_update(request, pk):
    if not can_manage_notifications(request.user):
        return redirect("notifications:list")

    notification = get_object_or_404(
        Notification,
        pk=pk,
        created_by__school_id=request.user.school_id,
    )

    if request.method == "POST":
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            return redirect("notifications:detail", pk=notification.pk)
    else:
        form = NotificationForm(instance=notification)

    return render(
        request,
        "notifications/notification_form.html",
        {
            "form": form,
            "page_title": "Edit Notification",
            "notification": notification,
        },
    )


@login_required
def notification_delete(request, pk):
    if not can_manage_notifications(request.user):
        return redirect("notifications:list")

    notification = get_object_or_404(
        Notification,
        pk=pk,
        created_by__school_id=request.user.school_id,
    )

    if request.method == "POST":
        notification.delete()
        return redirect("notifications:list")

    return render(
        request,
        "notifications/notification_confirm_delete.html",
        {"notification": notification},
    )


@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(
        visible_notifications(request.user),
        pk=pk,
    )

    NotificationRead.objects.get_or_create(
        notification=notification,
        user=request.user,
    )

    return redirect("notifications:detail", pk=notification.pk)
