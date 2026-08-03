from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [

    path("admin/", admin.site.urls),

    # Dashboard
    path("dashboard/", include("Apps.dashboard.urls")),

    # Authentication
    path("", include("accounts.urls")),

    # Students
    path("students/", include("Apps.students.urls")),

    # Guardians
    path("guardians/", include("Apps.guardians.urls")),

    #Teachers
    path("teachers/", include("Apps.teachers.urls")),

    # Leave Management
    path(
        "leave-management/",
         include("Apps.leave_management.urls"),
         ),

]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )