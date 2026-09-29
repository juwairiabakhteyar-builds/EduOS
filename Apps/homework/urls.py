from django.urls import path

from . import views


app_name = "homework"


urlpatterns = [
    path(
        "",
        views.homework_dashboard,
        name="dashboard",
    ),
    path(
        "assignments/",
        views.assignment_list,
        name="assignment_list",
    ),
    path(
        "assignments/create/",
        views.assignment_create,
        name="assignment_create",
    ),
    path(
        "assignments/<int:pk>/edit/",
        views.assignment_update,
        name="assignment_update",
    ),
    path(
        "assignments/<int:pk>/delete/",
        views.assignment_delete,
        name="assignment_delete",
    ),
]
