from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.attendance_dashboard,
        name="attendance_dashboard",
    ),

    path(
        "mark/",
        views.mark_attendance,
        name="mark_attendance",
    ),

    path(
        "records/",
        views.attendance_records,
        name="attendance_records",
    ),

    path(
        "<int:pk>/",
        views.attendance_detail,
        name="attendance_detail",
    ),

]