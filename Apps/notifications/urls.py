from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path("create/", views.notification_create, name="create"),
    path("<int:pk>/", views.notification_detail, name="detail"),
    path("<int:pk>/edit/", views.notification_update, name="edit"),
    path("<int:pk>/delete/", views.notification_delete, name="delete"),
    path("<int:pk>/read/", views.notification_mark_read, name="mark_read"),
]
