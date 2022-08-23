import datetime
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
import catalog
from catalog.forms import RenewBookForm
from catalog.models import Author, Book, BookInstance, Genre

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1
    num_genres = Genre.objects.count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_genres': num_genres,
    }
    return render(request, 'index.html', context)

class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 2
    template_name = 'book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    
"""
def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book Does Not Exist')
    return render(request, 'book_detail.html', context={'book':book})
    
    or you can  use a get_object_or_404() method
"""
    
class AuthorListView(ListView):
    model= Author
    paginate_by = 2
    template_name = 'author_list.html'

    
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'

class LoanedBookByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'borrowedbooks.html'
    paginate_by = 1
    login_url = 'login'
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class AllLoanedBooks(PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'all_borrowed_books.html'
    login_url = 'login'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
from django.contrib.auth.decorators import login_required, permission_required    

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
        return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
            'renewal_date': proposed_renewal_date
        })
        context= {
            'form':form,
            'book_instance': book_instance
        }
        return render(request, 'book_renew_librarian.html',context)
    
from .models import Author, Book

class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_birth': '11/06/2020'}
    template_name = 'author_form.html'
    permission_required = 'catalog.can_mark_returned'
    login_url = 'login'

    
class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    template_name = 'author_edit.html'
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    login_url = 'login'

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
    login_url = 'login'
    
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'
    login_url = 'login'
    permission_required= 'catalog.can_mark_returned'
    
class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'book_edit.html'
    fields = '__all__'
    permission_required= 'catalog.can_mark_returned'
    login_url = 'login'

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books')
    permission_required= 'catalog.can_mark_returned'
    login_url = 'login'