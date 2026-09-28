from django.conf import settings
from django.db import models


class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Book Category"
        verbose_name_plural = "Book Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(
        BookCategory,
        on_delete=models.PROTECT,
        related_name="books",
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    shelf_location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
        ]

    def __str__(self):
        return self.title


class LibraryMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="library_membership",
    )
    membership_id = models.CharField(max_length=50, unique=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["membership_id"]

    def __str__(self):
        return self.membership_id


class BookIssue(models.Model):
    STATUS_CHOICES = [
        ("issued", "Issued"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="issues",
    )
    member = models.ForeignKey(
        LibraryMember,
        on_delete=models.PROTECT,
        related_name="book_issues",
    )
    issued_date = models.DateField()
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="issued",
    )
    fine_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-issued_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return f"{self.book} - {self.member}"
