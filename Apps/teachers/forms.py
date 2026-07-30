from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "mobile_number",
            "email",
            "qualification",
            "experience",
            "joining_date",
            "designation",
            "photo",
            "address",
            "status",
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

            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "10",
                    "inputmode": "numeric",
                    "pattern": "[0-9]*",
                    "oninput": "this.value=this.value.replace(/[^0-9]/g,'').slice(0,10)"
                }
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "qualification": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "experience": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "designation": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

        }

    # --------------------------
    # Name Validation
    # --------------------------

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


    # --------------------------
    # Mobile Validation
    # --------------------------

    def clean_mobile_number(self):

        mobile = self.cleaned_data["mobile_number"]

        if not mobile.isdigit():
            raise ValidationError(
                "Mobile number must contain digits only."
            )

        if len(mobile) != 10:
            raise ValidationError(
                "Mobile number must be exactly 10 digits."
            )

        return mobile