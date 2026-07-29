from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.guardian_list,
        name="guardian_list",
    ),

    path(
        "add/",
        views.guardian_create,
        name="guardian_create",
    ),

    path(
        "<int:pk>/",
        views.guardian_detail,
        name="guardian_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.guardian_update,
        name="guardian_update",
    ),

    path(
        "<int:pk>/delete/",
        views.guardian_delete,
        name="guardian_delete",
    ),
]