from django import forms

from .models import HomeworkAssignment


class HomeworkAssignmentForm(forms.ModelForm):
    class Meta:
        model = HomeworkAssignment
        fields = [
            "title",
            "subject",
            "description",
            "teacher",
            "academic_session",
            "academic_level",
            "section",
            "assigned_date",
            "due_date",
            "attachment",
            "is_published",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter assignment title",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Mathematics",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter homework instructions...",
                }
            ),
            "teacher": forms.Select(
                attrs={"class": "form-select"}
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
            "assigned_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "attachment": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        assigned_date = cleaned_data.get("assigned_date")
        due_date = cleaned_data.get("due_date")

        if assigned_date and due_date and due_date < assigned_date:
            self.add_error(
                "due_date",
                "Due date cannot be earlier than the assigned date.",
            )

        return cleaned_data