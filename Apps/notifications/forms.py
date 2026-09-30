from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = [
            "title",
            "message",
            "priority",
            "audience",
            "published",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter notification title"}
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 7,
                    "placeholder": "Write your announcement..."
                }
            ),
        }
