from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import BookForm, BookIssueForm, LibraryMemberForm
from .models import Book, BookCategory, BookIssue, LibraryMember


User = get_user_model()


class LibraryModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = BookCategory.objects.create(
            name="Computer Science",
            description="Technology books",
        )

        cls.user = User.objects.create_user(
            username="library_student",
            password="testpass123",
        )

        cls.member = LibraryMember.objects.create(
            user=cls.user,
            membership_id="LIB-0001",
        )

        cls.book = Book.objects.create(
            category=cls.category,
            title="Django Fundamentals",
            author="Test Author",
            isbn="9780000000001",
            quantity=5,
            available_quantity=5,
        )

    def test_category_string(self):
        self.assertEqual(
            str(self.category),
            "Computer Science",
        )

    def test_book_string(self):
        self.assertEqual(
            str(self.book),
            "Django Fundamentals",
        )

    def test_member_string(self):
        self.assertEqual(
            str(self.member),
            "LIB-0001",
        )

    def test_issue_string(self):
        issue = BookIssue.objects.create(
            book=self.book,
            member=self.member,
            issued_date=date.today(),
            due_date=date.today() + timedelta(days=14),
        )

        self.assertEqual(
            str(issue),
            "Django Fundamentals - LIB-0001",
        )


class LibraryFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = BookCategory.objects.create(
            name="Science",
        )

        cls.user = User.objects.create_user(
            username="form_user",
            password="testpass123",
        )

        cls.member = LibraryMember.objects.create(
            user=cls.user,
            membership_id="LIB-0002",
        )

        cls.book = Book.objects.create(
            category=cls.category,
            title="Python Basics",
            author="Test Author",
            quantity=5,
            available_quantity=3,
        )

    def test_valid_book_form(self):
        form = BookForm(
            data={
                "category": self.category.pk,
                "title": "New Book",
                "author": "New Author",
                "isbn": "1234567890",
                "publisher": "Test Publisher",
                "publication_year": 2026,
                "quantity": 10,
                "available_quantity": 8,
                "shelf_location": "A-01",
                "description": "Test description",
                "is_active": True,
            }
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

    def test_available_quantity_cannot_exceed_quantity(self):
        form = BookForm(
            data={
                "category": self.category.pk,
                "title": "Invalid Book",
                "author": "Test Author",
                "quantity": 2,
                "available_quantity": 5,
                "is_active": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "available_quantity",
            form.errors,
        )

    def test_duplicate_library_member_user_is_rejected(self):
        form = LibraryMemberForm(
            data={
                "user": self.user.pk,
                "membership_id": "LIB-0099",
                "is_active": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "user",
            form.errors,
        )

    def test_issue_form_rejects_due_date_before_issue_date(self):
        form = BookIssueForm(
            data={
                "book": self.book.pk,
                "member": self.member.pk,
                "issued_date": "2026-09-20",
                "due_date": "2026-09-10",
                "fine_amount": "0",
                "notes": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "due_date",
            form.errors,
        )


class LibraryViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = BookCategory.objects.create(
            name="General",
        )

        cls.user = User.objects.create_user(
            username="library_user",
            password="testpass123",
        )

        cls.member = LibraryMember.objects.create(
            user=cls.user,
            membership_id="LIB-0003",
        )

        cls.book = Book.objects.create(
            category=cls.category,
            title="Django Web Development",
            author="Test Author",
            isbn="9999999999",
            publisher="Test Publisher",
            quantity=5,
            available_quantity=5,
        )

    def test_library_dashboard_requires_login(self):
        response = self.client.get(
            reverse("library:dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_book_list_requires_login(self):
        response = self.client.get(
            reverse("library:book_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_issue_list_requires_login(self):
        response = self.client.get(
            reverse("library:issue_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_library_dashboard_loads(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        response = self.client.get(
            reverse("library:dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertContains(
            response,
            "Library",
        )

    def test_book_list_loads(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        response = self.client.get(
            reverse("library:book_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertContains(
            response,
            "Django Web Development",
        )

    def test_book_search(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        response = self.client.get(
            reverse("library:book_list"),
            {"q": "Django"},
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertContains(
            response,
            "Django Web Development",
        )

    def test_issue_create_reduces_available_quantity(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        response = self.client.post(
            reverse("library:issue_create"),
            {
                "book": self.book.pk,
                "member": self.member.pk,
                "issued_date": date.today().isoformat(),
                "due_date": (
                    date.today() + timedelta(days=14)
                ).isoformat(),
                "fine_amount": "0",
                "notes": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("library:issue_list"),
        )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_quantity,
            4,
        )

        self.assertTrue(
            BookIssue.objects.filter(
                book=self.book,
                member=self.member,
                status="issued",
            ).exists()
        )

    def test_issue_return_increases_available_quantity(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        self.book.available_quantity = 4
        self.book.save(update_fields=["available_quantity"])

        issue = BookIssue.objects.create(
            book=self.book,
            member=self.member,
            issued_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status="issued",
            fine_amount=Decimal("0.00"),
        )

        response = self.client.post(
            reverse(
                "library:issue_return",
                kwargs={"pk": issue.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse("library:issue_list"),
        )

        issue.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(
            issue.status,
            "returned",
        )
        self.assertEqual(
            issue.returned_date,
            date.today(),
        )
        self.assertEqual(
            self.book.available_quantity,
            5,
        )

    def test_unavailable_book_cannot_be_issued(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        self.book.available_quantity = 0
        self.book.save(update_fields=["available_quantity"])

        response = self.client.post(
            reverse("library:issue_create"),
            {
                "book": self.book.pk,
                "member": self.member.pk,
                "issued_date": date.today().isoformat(),
                "due_date": (
                    date.today() + timedelta(days=14)
                ).isoformat(),
                "fine_amount": "0",
                "notes": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            BookIssue.objects.filter(
                book=self.book,
                member=self.member,
            ).exists()
        )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_quantity,
            0,
        )

    def test_book_delete_soft_deactivates_book(self):
        self.client.login(
            username="library_user",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "library:book_delete",
                kwargs={"pk": self.book.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse("library:book_list"),
        )

        self.book.refresh_from_db()

        self.assertFalse(
            self.book.is_active
        )
