from datetime import date, timedelta

from django import forms
from django.contrib.auth import get_user_model

from .models import Book, BookCategory, BookIssue, LibraryMember


User = get_user_model()


class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional description",
                }
            ),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "category",
            "title",
            "author",
            "isbn",
            "publisher",
            "publication_year",
            "quantity",
            "available_quantity",
            "shelf_location",
            "description",
            "is_active",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "publisher": forms.TextInput(attrs={"class": "form-control"}),
            "publication_year": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "available_quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "shelf_location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        available_quantity = cleaned_data.get("available_quantity")

        if quantity is not None and available_quantity is not None:
            if available_quantity > quantity:
                self.add_error(
                    "available_quantity",
                    "Available quantity cannot be greater than total quantity.",
                )

        return cleaned_data


class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ["user", "membership_id", "is_active"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "membership_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. LIB-0001",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(
            is_active=True
        ).order_by("username")

    def clean_user(self):
        user = self.cleaned_data["user"]
        existing = LibraryMember.objects.filter(user=user)

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "This user already has a library membership."
            )

        return user


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = [
            "book",
            "member",
            "issued_date",
            "due_date",
            "fine_amount",
            "notes",
        ]
        widgets = {
            "book": forms.Select(attrs={"class": "form-select"}),
            "member": forms.Select(attrs={"class": "form-select"}),
            "issued_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fine_amount": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "step": "0.01"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["book"].queryset = Book.objects.filter(
            is_active=True,
            available_quantity__gt=0,
        ).select_related("category").order_by("title")

        self.fields["member"].queryset = LibraryMember.objects.filter(
            is_active=True,
        ).select_related("user").order_by("membership_id")

        if not self.instance.pk:
            self.fields["issued_date"].initial = date.today()
            self.fields["due_date"].initial = date.today() + timedelta(days=14)

    def clean(self):
        cleaned_data = super().clean()
        issued_date = cleaned_data.get("issued_date")
        due_date = cleaned_data.get("due_date")

        if issued_date and due_date and due_date < issued_date:
            self.add_error(
                "due_date",
                "Due date cannot be earlier than the issue date.",
            )

        return cleaned_data
