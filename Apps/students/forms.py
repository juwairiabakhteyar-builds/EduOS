from django import forms

from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "student_id",
            "admission_number",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "photo",
            "academic_session",
            "academic_level",
            "section",
            "guardian",
        ]