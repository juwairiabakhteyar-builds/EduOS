from django import forms

from .models import Student
from Apps.guardians.models import Guardian

from django.core.exceptions import ValidationError
import re

class StudentForm(forms.ModelForm):

    guardian_first_name = forms.CharField(
        max_length=100,
        label="Guardian First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )

    guardian_last_name = forms.CharField(
        max_length=100,
        required=False,
        label="Guardian Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
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
        max_length=15,
        label="Mobile Number",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )

    guardian_email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
    )

    guardian_occupation = forms.CharField(
        required=False,
        label="Occupation",
        widget=forms.TextInput(
            attrs={"class": "form-control"}
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
            "guardian",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "middle_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
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

            "guardian": forms.HiddenInput(),

        }

        labels = {

            "date_of_birth": "Date of Birth",
            "academic_level": "Academic Level",

        }

    # -------------------------
    # Validation
    # -------------------------

    def clean_first_name(self):

        value = self.cleaned_data["first_name"].strip()

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValidationError(
                "First name can contain only letters."
            )

        return value


    def clean_middle_name(self):

        value = self.cleaned_data["middle_name"].strip()

        if value and not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValidationError(
                "Middle name can contain only letters."
            )

        return value


    def clean_last_name(self):

        value = self.cleaned_data["last_name"].strip()

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValidationError(
                "Last name can contain only letters."
            )

        return value


    def clean_guardian_first_name(self):

        value = self.cleaned_data["guardian_first_name"].strip()

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValidationError(
                "Guardian first name can contain only letters."
            )

        return value


    def clean_guardian_last_name(self):

        value = self.cleaned_data["guardian_last_name"].strip()

        if value and not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValidationError(
                "Guardian last name can contain only letters."
            )

        return value


    def clean_guardian_mobile(self):

        mobile = self.cleaned_data["guardian_mobile"]

        if not mobile.isdigit():
            raise ValidationError(
                "Mobile number must contain digits only."
            )

        if len(mobile) != 10:
            raise ValidationError(
                "Mobile number must be exactly 10 digits."
            )

        return mobile