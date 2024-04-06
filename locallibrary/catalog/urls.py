from django.urls import path, include  # You only need to import 'path' and 'include' once
from . import views
from .views import LoanedBooksAllListView 
from django.urls import path
from .views import AuthorCreate  # Ensure you import the view

urlpatterns = [
    # Your existing URL patterns...
    path('author/create/', AuthorCreate.as_view(), name='author-create'),
    # Add this line for the 'author-create' path
]

urlpatterns = [
    # Home page of the catalog app
    path('', views.index, name='index'),
    
    # Book URLs
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='authors'),

    # URLs for loaned books by user
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    # Add Django site authentication urls (for login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('all-borrowed/', LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('author/create/', AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
