from django import forms

from .models import Exam, ExamResult, ExamSubject


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            "name",
            "academic_session",
            "academic_level",
            "start_date",
            "end_date",
            "is_published",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Mid Term Examination",
                }
            ),
            "academic_session": forms.Select(
                attrs={"class": "form-select"}
            ),
            "academic_level": forms.Select(
                attrs={"class": "form-select"}
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }


class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = ExamSubject
        fields = [
            "name",
            "exam_date",
            "max_marks",
            "passing_marks",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Mathematics",
                }
            ),
            "exam_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "max_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
            "passing_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = [
            "student",
            "subject",
            "marks_obtained",
            "remarks",
        ]
        widgets = {
            "student": forms.Select(
                attrs={"class": "form-select"}
            ),
            "subject": forms.Select(
                attrs={"class": "form-select"}
            ),
            "marks_obtained": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional remarks",
                }
            ),
        }
