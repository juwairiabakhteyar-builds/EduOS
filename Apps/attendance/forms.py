from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = [
            "person",
            "attendance_date",
            "status",
            "remarks",
        ]

        widgets = {

            "person": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "attendance_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional remarks...",
                }
            ),

        }