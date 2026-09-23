from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Student
from Apps.guardians.models import Guardian
from Apps.academics.models import Section


class StudentForm(forms.ModelForm):

    guardian_first_name = forms.CharField(
        max_length=100,
        label="Guardian First Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter first name",
            }
        ),
    )

    guardian_last_name = forms.CharField(
        max_length=100,
        required=False,
        label="Guardian Last Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter last name",
            }
        ),
    )

    guardian_relationship = forms.ChoiceField(
        choices=Guardian.RELATIONSHIP_CHOICES,
        label="Relationship",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    guardian_mobile = forms.CharField(
        max_length=10,
        label="Mobile Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "10-digit mobile number",
                "maxlength": "10",
                "inputmode": "numeric",
                "autocomplete": "tel",
            }
        ),
    )

    guardian_email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "guardian@example.com",
                "autocomplete": "email",
            }
        ),
    )

    guardian_occupation = forms.CharField(
        required=False,
        label="Occupation",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Occupation",
            }
        ),
    )

    class Meta:
        model = Student

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "photo",
            "academic_session",
            "academic_level",
            "section",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter first name",
                    "autocomplete": "given-name",
                }
            ),

            "middle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Middle name (optional)",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter last name",
                    "autocomplete": "family-name",
                }
            ),

            "gender": forms.Select(
                attrs={"class": "form-select"}
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "academic_session": forms.Select(
                attrs={"class": "form-select"}
            ),

            "academic_level": forms.Select(
                attrs={"class": "form-select"}
            ),

            "section": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

        labels = {
            "first_name": "First Name",
            "middle_name": "Middle Name",
            "last_name": "Last Name",
            "date_of_birth": "Date of Birth",
            "academic_session": "Academic Session",
            "academic_level": "Academic Level",
            "section": "Section",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["section"].queryset = (
            Section.objects.all().order_by("name")
        )

        # Populate guardian information while editing.
        if self.instance and self.instance.pk and self.instance.guardian:
            guardian = self.instance.guardian

            self.fields["guardian_first_name"].initial = guardian.first_name
            self.fields["guardian_last_name"].initial = guardian.last_name
            self.fields["guardian_relationship"].initial = guardian.relationship
            self.fields["guardian_mobile"].initial = guardian.mobile_number
            self.fields["guardian_email"].initial = guardian.email
            self.fields["guardian_occupation"].initial = guardian.occupation

    # -------------------------
    # Name validation
    # -------------------------

    def _validate_name(self, value, field_name, required=True):
        value = value.strip()

        if not value and required:
            raise ValidationError(
                f"{field_name} is required."
            )

        if value and not re.fullmatch(r"[A-Za-z\s'-]+", value):
            raise ValidationError(
                f"{field_name} can contain only letters, spaces, apostrophes and hyphens."
            )

        return value

    def clean_first_name(self):
        return self._validate_name(
            self.cleaned_data["first_name"],
            "First name",
        )

    def clean_middle_name(self):
        return self._validate_name(
            self.cleaned_data.get("middle_name", ""),
            "Middle name",
            required=False,
        )

    def clean_last_name(self):
        return self._validate_name(
            self.cleaned_data["last_name"],
            "Last name",
        )

    def clean_guardian_first_name(self):
        return self._validate_name(
            self.cleaned_data["guardian_first_name"],
            "Guardian first name",
        )

    def clean_guardian_last_name(self):
        return self._validate_name(
            self.cleaned_data.get("guardian_last_name", ""),
            "Guardian last name",
            required=False,
        )

    # -------------------------
    # Guardian mobile
    # -------------------------

    def clean_guardian_mobile(self):
        mobile = self.cleaned_data["guardian_mobile"].strip()

        if not mobile.isdigit():
            raise ValidationError(
                "Mobile number must contain digits only."
            )

        if len(mobile) != 10:
            raise ValidationError(
                "Mobile number must be exactly 10 digits."
            )

        return mobile

    # -------------------------
    # Date of birth
    # -------------------------

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]

        from django.utils import timezone

        if dob >= timezone.localdate():
            raise ValidationError(
                "Date of birth must be earlier than today."
            )

        return dob