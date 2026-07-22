from django.contrib import admin

from .models import (
    AcademicSession,
    AcademicLevel,
    Section,
)

admin.site.register(AcademicSession)
admin.site.register(AcademicLevel)
admin.site.register(Section)