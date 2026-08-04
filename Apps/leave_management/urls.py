from django.urls import path

from . import views


urlpatterns = [

    # =====================================
    # Leave Types
    # =====================================

    path(
        "",
        views.leave_type_list,
        name="leave_type_list",
    ),

    path(
        "add/",
        views.leave_type_create,
        name="leave_type_create",
    ),

    path(
        "<int:pk>/",
        views.leave_type_detail,
        name="leave_type_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.leave_type_update,
        name="leave_type_update",
    ),

    path(
        "<int:pk>/delete/",
        views.leave_type_delete,
        name="leave_type_delete",
    ),

    # =====================================
    # Leave Applications
    # =====================================

    path(
        "applications/",
        views.leave_application_list,
        name="leave_application_list",
    ),

    path(
        "applications/add/",
        views.leave_application_create,
        name="leave_application_create",
    ),

    path(
        "applications/<int:pk>/",
        views.leave_application_detail,
        name="leave_application_detail",
    ),

    path(
    "applications/<int:pk>/approve/",
    views.leave_application_approve,
    name="leave_application_approve",
    ),

    path(
        "applications/<int:pk>/reject/",
        views.leave_application_reject,
        name="leave_application_reject",
    ),

    path(
        "applications/<int:pk>/cancel/",
        views.leave_application_cancel,
        name="leave_application_cancel",
    ),

]