from django.urls import path
from . import views

urlpatterns = [
    # with name='index' you can refer to this in html to redirect more easily (you have to do that with reverse??)
    path('', views.index, name='index'),
    # For Django class-based views we access an appropriate view function by calling the class method as_view(). 
    # This does all the work of creating an instance of the class, and making sure that the right handler methods are called for incoming HTTP requests.
    path('books/', views.BookListView.as_view(), name='books'),
    # pk is the variable name, int is a converter (optional)
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allborrowedbooks/', views.AllBorrowedBooksView.as_view(), name='all-borrowed-books'),
    # The URL configuration will redirect URLs with the format /catalog/book/<bookinstance_id>/renew/ to 
    # the function named renew_book_librarian() in views.py, and send the BookInstance id as the parameter named pk.
    # Note: We can name our captured URL data "pk" anything we like, because we have complete control over the view 
    # function (we're not using a generic detail view class that expects parameters with a certain name). 
    # However, pk short for "primary key", is a reasonable convention to use!
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]