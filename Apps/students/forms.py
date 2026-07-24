from django import forms

from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "student_id",
            "admission_number",
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

            "student_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "STU0001"
            }),

            "admission_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ADM2026001"
            }),

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "middle_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "academic_session": forms.Select(attrs={
                "class": "form-select"
            }),

            "academic_level": forms.Select(attrs={
                "class": "form-select"
            }),

            "section": forms.Select(attrs={
                "class": "form-select"
            }),

            "guardian": forms.Select(attrs={
                "class": "form-select"
            }),
        }

        labels = {
            "student_id": "Student ID",
            "admission_number": "Admission Number",
            "date_of_birth": "Date of Birth",
            "academic_level": "Academic Level",
        }