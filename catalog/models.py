from django.db import models
from django.urls import reverse

# Required for unique book instances
import uuid

# import this so the User is available to subsequent code that makes use of it
from django.contrib.auth.models import User
from datetime import date


class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(
        max_length=20, help_text="Enter field documentation"
    )
    # …

    # Metadata
    class Meta:
        ordering = ["-my_field_name"]

    # Methods

    # Note: Assuming you will use URLs like /myapplication/mymodelname/2 to display individual records for your model
    # (where "2" is the id for a particular record), you will need to create a URL mapper to pass the response and id
    # to a "model detail view" (which will do the work required to display the record). The reverse() function  is
    # able to "reverse" your URL mapper (in the above case named 'model-detail-view') in order to create a URL of the
    # right format. Of course to make this work you still have to write the URL mapping, view, and template!
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("model-detail-view", args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    # on_delete=models.SET_NULL, which will set the value of the book's author field to Null if the associated author record is deleted.
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.CharField(max_length=30, default="")

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse("book-detail", args=[str(self.id)])

    # this is for the admin panel to displaying genres for the books in view mode
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    # The key specifies on_delete=models.RESTRICT to ensure that the Book cannot be deleted while referenced by a BookInstance.
    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        # the second parameter is only for information
        permissions = (("can_mark_returned", "Set book as returned"),)

    # Determines if the book is overdue based on due date and current date.
    def is_overdue(self):
        # The following code uses Python's bool() function, which evaluates an
        # object or the resulting object of an expression, and returns True unless
        # the result is "falsy", in which case it returns False. In Python an object
        # is falsy (evaluates as False) if it is: empty (like [], (), {}), 0, None or
        # if it is False.
        return bool(self.due_back and date.today() > self.due_back)
        # this line will first checks if self.due_back is truthy (i.e. not None or False),
        # and only then evaluates the comparison date.today() > self.due_back.
        # This means that if self.due_back is falsy, the comparison will not be
        # evaluated and the method will return False without any error.
        # An empty due_back field would cause Django to throw an error instead of
        # showing the page: empty values are not comparable.

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"
