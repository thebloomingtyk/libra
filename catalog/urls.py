from django.urls import path
from . import views
from .views import AuthorCreateView, AuthorDeleteView, AuthorUpdateView, BookCreateView, BookDeleteView, BookListView, BookDetailView, AuthorListView, AuthorDetailView, BookUpdateView, LoanedBookByUserListView, AllLoanedBooks

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('books-borrowed/', AllLoanedBooks.as_view(), name='all-borrowed'), #permission_required
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,name='renew-book-librarian'), #permission_required
    path('author/create/', AuthorCreateView.as_view(), name='author-create'), #permission_required
    path('author/<int:pk>/update/', AuthorUpdateView.as_view(), name='author-update'), #permission_required
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'), #permission_required
    path('book/create/', BookCreateView.as_view(), name='book-create'), #permission_required
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), #permission_required
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), #permission_required
]
