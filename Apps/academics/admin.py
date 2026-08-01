from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
import re

from .models import (
    AcademicSession,
    AcademicLevel,
    Section,
)

# ==========================================
# Academic Session Admin Form
# ==========================================

class AcademicSessionAdminForm(forms.ModelForm):

    class Meta:

        model = AcademicSession

        fields = "__all__"

    def clean_name(self):

        value = self.cleaned_data["name"].strip()

        # Accept only formats like:
        # 2024-2025
        # 2025-2026

        if not re.fullmatch(r"\d{4}-\d{4}", value):

            raise ValidationError(
                "Session must be in YYYY-YYYY format (Example: 2024-2025)."
            )

        start, end = value.split("-")

        if int(end) != int(start) + 1:

            raise ValidationError(
                "Ending year must be exactly one year after the starting year."
            )

        return value

# ==========================================
# Academic Level Admin Form
# ==========================================

class AcademicLevelAdminForm(forms.ModelForm):

    class Meta:

        model = AcademicLevel

        fields = "__all__"

    def clean_name(self):

        value = self.cleaned_data["name"].strip()

        if not re.fullmatch(
            r"(Nursery|LKG|UKG|[1-9]|10|11|12)",
            value,
        ):

            raise ValidationError(
                "Enter Nursery, LKG, UKG or Class 1-12."
            )

        return value

# ==========================================
# Section Admin Form
# ==========================================

class SectionAdminForm(forms.ModelForm):

    class Meta:

        model = Section

        fields = "__all__"

    def clean_name(self):

        value = self.cleaned_data["name"].strip().upper()

        if not re.fullmatch(r"[A-Z]", value):

            raise ValidationError(
                "Section must be a single letter like A, B or C."
            )

        return value

# ==========================================
# Academic Session
# ==========================================

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):

    form = AcademicSessionAdminForm

    list_display = (
        "name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

# ==========================================
# Academic Level
# ==========================================

@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):

    form = AcademicLevelAdminForm

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

# ==========================================
# Section
# ==========================================

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    form = SectionAdminForm

    list_display = (
        "academic_level",
        "name",
    )

    list_filter = (
        "academic_level",
    )

    search_fields = (
        "name",
    )