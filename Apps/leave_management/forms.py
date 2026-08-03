from django import forms
from django.core.exceptions import ValidationError
import re

from .models import LeaveType


class LeaveTypeForm(forms.ModelForm):

    class Meta:

        model = LeaveType

        fields = [
            "leave_name",
            "leave_code",
            "maximum_days",
            "is_paid",
            "description",
            "status",
        ]

        widgets = {

            "leave_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "leave_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform:uppercase;",
                }
            ),

            "maximum_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "is_paid": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def clean_leave_name(self):

        name = self.cleaned_data["leave_name"].strip()

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise ValidationError(
                "Leave name can contain only letters and spaces."
            )

        return name

    def clean_leave_code(self):

        code = self.cleaned_data["leave_code"].strip().upper()

        if not re.fullmatch(r"[A-Z]{2,5}", code):
            raise ValidationError(
                "Leave code must contain 2 to 5 uppercase letters."
            )

        return code