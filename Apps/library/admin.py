from django.contrib import admin

from .models import Book, BookCategory, BookIssue, LibraryMember


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "quantity",
        "available_quantity",
        "is_active",
    )
    list_filter = ("category", "is_active", "publication_year")
    search_fields = ("title", "author", "isbn", "publisher")
    list_editable = ("available_quantity", "is_active")


@admin.register(LibraryMember)
class LibraryMemberAdmin(admin.ModelAdmin):
    list_display = (
        "membership_id",
        "user",
        "joined_date",
        "is_active",
    )
    list_filter = ("is_active", "joined_date")
    search_fields = (
        "membership_id",
        "user__username",
        "user__first_name",
        "user__last_name",
    )


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "member",
        "issued_date",
        "due_date",
        "returned_date",
        "status",
        "fine_amount",
    )
    list_filter = ("status", "issued_date", "due_date")
    search_fields = (
        "book__title",
        "member__membership_id",
    )
    date_hierarchy = "issued_date"