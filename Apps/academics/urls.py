from django.urls import path

from . import views

urlpatterns = [
    path("", views.academics_dashboard, name="academics_dashboard"),

    path("sessions/add/", views.session_create, name="academic_session_add"),
    path(
        "sessions/<int:pk>/edit/",
        views.session_update,
        name="academic_session_edit",
    ),
    path(
        "sessions/<int:pk>/delete/",
        views.session_delete,
        name="academic_session_delete",
    ),

    path("levels/add/", views.level_create, name="academic_level_add"),
    path(
        "levels/<int:pk>/edit/",
        views.level_update,
        name="academic_level_edit",
    ),
    path(
        "levels/<int:pk>/delete/",
        views.level_delete,
        name="academic_level_delete",
    ),

    path("sections/add/", views.section_create, name="academic_section_add"),
    path(
        "sections/<int:pk>/edit/",
        views.section_update,
        name="academic_section_edit",
    ),
    path(
        "sections/<int:pk>/delete/",
        views.section_delete,
        name="academic_section_delete",
    ),
]
