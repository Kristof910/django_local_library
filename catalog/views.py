from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookModelForm
from catalog.models import BookInstance
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # custom (I wrote this)
    all_genres = Genre.objects.all()
    custom_genre_counter = 0
    for genre in all_genres:
        if genre.name[0] == "r":
            custom_genre_counter += 1

    # Number of visits to this view, as counted in the session variable.
    # this line will request the num_visists variable from the session IF not present then it will create one with the 0 as a default value
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "all_genres": custom_genre_counter,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


# this will generate a generic view and do a lot of stuff automatically
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    # with this only you can basically create pagination
    paginate_by = 1

    # THESE ARE OPTIONAL FOR REPRESENTATION
    # your own name for the list as a template variable
    # context_object_name = 'book_list'
    # Get 5 books containing the title war
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # Specify your own template name/location
    # template_name = 'books/my_arbitrary_template_name_list.html'


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        # o = on loan
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class AllBorrowedBooksView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.ListView
):
    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/all_borrowed_books.html"


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("all-borrowed-books"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


# these are automatizations of the create/update/delete


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {"date_of_death": "11/06/2020"}


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    fields = (
        "__all__"  # Not recommended (potential security issue if more fields added)
    )


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy("authors")


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = ["title", "author", "summary", "isbn", "genre", "language"]


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = (
        "__all__"  # Not recommended (potential security issue if more fields added)
    )


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy("books")
