from django import forms
from django.core.exceptions import ValidationError
import re

from .models import AcademicSession, AcademicLevel, Section


ALLOWED_LEVELS = [
    "Nursery",
    "LKG",
    "UKG",
    *[f"Class {i}" for i in range(1, 13)],
]


class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ["name", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "2026-2027"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if not re.fullmatch(r"\d{4}-\d{4}", value):
            raise ValidationError(
                "Session must be in YYYY-YYYY format, for example 2026-2027."
            )
        start, end = value.split("-")
        if int(end) != int(start) + 1:
            raise ValidationError(
                "Ending year must be exactly one year after the starting year."
            )
        return value


class AcademicLevelForm(forms.ModelForm):
    class Meta:
        model = AcademicLevel
        fields = ["name"]
        widgets = {
            "name": forms.Select(
                attrs={"class": "form-select"},
                choices=[("", "Select academic level")]
                + [(level, level) for level in ALLOWED_LEVELS],
            )
        }

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if value not in ALLOWED_LEVELS:
            raise ValidationError("Select Nursery, LKG, UKG or Class 1-12.")
        return value


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "A", "maxlength": 1}
            )
        }

    def clean_name(self):
        value = self.cleaned_data["name"].strip().upper()
        if not re.fullmatch(r"[A-Z]", value):
            raise ValidationError("Section must be a single letter such as A, B or C.")
        return value
