from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm

def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(ListView):
    model = Book
    paginate_by = 2

class BookDetailView(DetailView):
    model = Book

class AuthorListView(ListView):
    model = Author
    # Specify the template only if you're not using the default "author_list.html"
    # template_name = 'catalog/author_list.html'

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


# In your catalog/views.py

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_all.html'  # Ensure you have this template
    queryset = BookInstance.objects.filter(status__exact='o').order_by('due_back')
from django.views.generic.edit import CreateView
from .models import Author
from django.urls import reverse_lazy

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'  # Specify the fields you want to include in your form, or use '__all__' to include all fields
    initial = {'date_of_death': '11/06/2020'}  # You can set initial field values with a dictionary
    template_name = 'catalog/author_form.html'  # Define your template
    success_url = reverse_lazy('authors')  # Redirect after successful author creation


from django.views.generic import DetailView
from .models import Author

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'  # Ensure you have this template
