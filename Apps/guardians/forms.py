from django import forms

from .models import Guardian


class GuardianForm(forms.ModelForm):

    class Meta:
        model = Guardian

        fields = [
            "first_name",
            "last_name",
            "relationship",
            "mobile_number",
            "email",
            "occupation",
        ]

        widgets = {

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "relationship": forms.Select(attrs={
                "class": "form-select"
            }),

            "mobile_number": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "occupation": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }