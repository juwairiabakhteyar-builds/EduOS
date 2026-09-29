from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("create/", views.exam_create, name="exam_create"),
    path("<int:pk>/", views.exam_detail, name="exam_detail"),
    path("<int:pk>/edit/", views.exam_update, name="exam_update"),
    path("<int:pk>/delete/", views.exam_delete, name="exam_delete"),
    path(
        "<int:exam_pk>/subjects/add/",
        views.subject_create,
        name="subject_create",
    ),
    path(
        "<int:exam_pk>/results/add/",
        views.result_create,
        name="result_create",
    ),
]
