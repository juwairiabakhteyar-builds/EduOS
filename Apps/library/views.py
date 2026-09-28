from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BookCategoryForm,
    BookForm,
    BookIssueForm,
    LibraryMemberForm,
)
from .models import Book, BookCategory, BookIssue, LibraryMember


@login_required
def library_dashboard(request):
    books = Book.objects.filter(is_active=True)

    context = {
        "total_books": books.count(),
        "total_copies": sum(book.quantity for book in books),
        "available_copies": sum(book.available_quantity for book in books),
        "issued_books": BookIssue.objects.filter(status="issued").count(),
        "overdue_books": BookIssue.objects.filter(status="overdue").count(),
        "recent_issues": BookIssue.objects.select_related(
            "book", "member", "member__user"
        )[:10],
    }
    return render(request, "library/dashboard.html", context)


@login_required
def book_list(request):
    query = request.GET.get("q", "").strip()

    books = Book.objects.filter(is_active=True).select_related("category")

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(isbn__icontains=query)
            | Q(publisher__icontains=query)
        )

    return render(
        request,
        "library/book_list.html",
        {"books": books, "query": query},
    )


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect("library:book_list")
    else:
        form = BookForm()

    return render(
        request,
        "library/form.html",
        {"form": form, "title": "Add Book", "cancel_url": "library:book_list"},
    )


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect("library:book_list")
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "library/form.html",
        {"form": form, "title": "Edit Book", "cancel_url": "library:book_list"},
    )


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.is_active = False
        book.save(update_fields=["is_active"])
        messages.success(request, "Book removed from the active library.")
        return redirect("library:book_list")

    return render(
        request,
        "library/delete.html",
        {
            "object": book,
            "title": "Remove Book",
            "cancel_url": "library:book_list",
        },
    )


@login_required
def category_list(request):
    categories = BookCategory.objects.all()
    return render(
        request,
        "library/category_list.html",
        {"categories": categories},
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = BookCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book category added successfully.")
            return redirect("library:category_list")
    else:
        form = BookCategoryForm()

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Add Book Category",
            "cancel_url": "library:category_list",
        },
    )


@login_required
def member_list(request):
    members = LibraryMember.objects.select_related("user")
    return render(
        request,
        "library/member_list.html",
        {"members": members},
    )


@login_required
def member_create(request):
    if request.method == "POST":
        form = LibraryMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Library member added successfully.")
            return redirect("library:member_list")
    else:
        form = LibraryMemberForm()

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Add Library Member",
            "cancel_url": "library:member_list",
        },
    )


@login_required
def member_update(request, pk):
    member = get_object_or_404(LibraryMember, pk=pk)

    if request.method == "POST":
        form = LibraryMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Library member updated successfully.")
            return redirect("library:member_list")
    else:
        form = LibraryMemberForm(instance=member)

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Edit Library Member",
            "cancel_url": "library:member_list",
        },
    )


@login_required
def issue_list(request):
    issues = BookIssue.objects.select_related(
        "book", "member", "member__user"
    )

    status = request.GET.get("status", "").strip()
    if status in {"issued", "returned", "overdue"}:
        issues = issues.filter(status=status)

    return render(
        request,
        "library/issue_list.html",
        {"issues": issues, "status": status},
    )


@login_required
def issue_create(request):
    if request.method == "POST":
        form = BookIssueForm(request.POST)

        if form.is_valid():
            book_id = form.cleaned_data["book"].pk

            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=book_id)

                if not book.is_active or book.available_quantity <= 0:
                    form.add_error(
                        "book",
                        "This book is currently unavailable.",
                    )
                else:
                    issue = form.save(commit=False)
                    issue.status = "issued"
                    issue.save()

                    book.available_quantity -= 1
                    book.save(update_fields=["available_quantity"])

                    messages.success(
                        request,
                        f'"{book.title}" issued successfully.',
                    )
                    return redirect("library:issue_list")
    else:
        form = BookIssueForm()

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Issue Book",
            "cancel_url": "library:issue_list",
        },
    )


@login_required
def issue_return(request, pk):
    issue = get_object_or_404(
        BookIssue.objects.select_related("book", "member"),
        pk=pk,
    )

    if request.method == "POST":
        with transaction.atomic():
            locked_issue = BookIssue.objects.select_for_update().select_related(
                "book"
            ).get(pk=issue.pk)

            if locked_issue.status == "returned":
                messages.info(request, "This book has already been returned.")
                return redirect("library:issue_list")

            book = Book.objects.select_for_update().get(pk=locked_issue.book_id)

            locked_issue.status = "returned"
            locked_issue.returned_date = date.today()
            locked_issue.save(
                update_fields=["status", "returned_date"]
            )

            book.available_quantity = min(
                book.quantity,
                book.available_quantity + 1,
            )
            book.save(update_fields=["available_quantity"])

        messages.success(request, "Book returned successfully.")
        return redirect("library:issue_list")

    return render(
        request,
        "library/return_confirm.html",
        {"issue": issue},
    )
