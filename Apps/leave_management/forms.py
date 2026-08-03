from django import forms

from .models import LeaveType, LeaveApplication


# ======================================================
# Leave Type Form
# ======================================================

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
                }
            ),

            "maximum_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
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


# ======================================================
# Leave Application Form
# ======================================================

class LeaveApplicationForm(forms.ModelForm):

    class Meta:

        model = LeaveApplication

        fields = [
            "leave_type",
            "from_date",
            "to_date",
            "reason",
        ]

        widgets = {

            "leave_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "from_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "to_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter the reason for leave...",
                }
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:

            if to_date < from_date:

                raise forms.ValidationError(
                    "To Date cannot be earlier than From Date."
                )

        return cleaned_data