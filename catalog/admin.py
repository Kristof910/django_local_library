from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)

class BookInline(admin.TabularInline):
    model = Book

# Register the Admin classes for Author using the decorator
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # this will make columns for this infos, otherwise it will be only sorted by name
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # this is for the creating/editing page -> in what order to display or do combine the options into 1 line
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

# this and the inline in BookAdmin class is refering to when creating a new book you can also add instances to the other model at the same page
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]    

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'imprint', 'due_back', 'status', 'borrower')
    list_filter = ('status', 'due_back')

    # seperate the create/edit page so it will have 2 sections (for design only)
    fieldsets = (
        # None means it doesn't have a title of the section
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        # Availability is the title here
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )