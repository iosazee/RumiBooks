from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Book
from .forms import CategoryForm, BookForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'



class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = '/categories/'

    def form_valid(self, form):
        form.save()  # Save the form if it's valid
        success_message = 'Category created successfully.'
        messages.success(self.request, success_message)
        return redirect(self.success_url)

    def form_invalid(self, form):
        error_message = 'Category creation failed. Please check the form for errors.'
        messages.error(self.request, error_message)
        return super().form_invalid(form)



class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = '/categories/'

    def form_valid(self, form):
        form.save()
        success_message = 'Category updated successfully.'
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'Category update failed. Please check the form for errors.'
        messages.error(self.request, error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url



class CustomCategoryDeleteView(View):
    model = Category
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')

    def get(self, request, pk):
        category = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'category': category})

    def post(self, request, pk):
        category = get_object_or_404(self.model, pk=pk)
        category_name = category.name
        category.delete()

        success_message = f'Book "{category_name}" has been deleted.'
        messages.success(request, success_message)

        return redirect(self.success_url)






class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    paginate_by = 9  # Set the number of items per page

    def get_queryset(self):
        return Book.objects.all().order_by('-id')  # You can change the ordering as needed



class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'



class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    # success_url = '/books/'

    def form_valid(self, form):
        form.save()  # Save the form if it's valid
        success_message = 'Book created successfully.'
        messages.success(self.request, success_message)
        return redirect('/books/')

    def form_invalid(self, form):
        error_message = 'Book creation failed. Please check the form for errors.'
        messages.error(self.request, error_message)
        return super().form_invalid(form)




class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('book_list')


    def form_valid(self, form):
        form.save()
        success_message = 'Book updated successfully.'
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'Book update failed. Please check the form for errors.'
        messages.error(self.request, error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url


class CustomBookDeleteView(View):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('book_list')

    def get(self, request, pk):
        book = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(self.model, pk=pk)
        book_title = book.title
        book.delete()

        success_message = f'Book "{book_title}" has been deleted.'
        messages.success(request, success_message)

        return redirect(self.success_url)




def expense_report(request):
    # Retrieve the categories
    categories = Category.objects.all()

    # Create a list to store the expense data for each category
    category_expenses = []

    # Calculate total expenses for each category
    for category in categories:
        books_in_category = Book.objects.filter(category=category)
        total_expense = sum(book.distribution_expense for book in books_in_category)
        category_expenses.append({'category': category, 'total_expense': total_expense})

    context = {'category_expenses': category_expenses}
    return render(request, 'report/expense_report.html', context)



def expense_chartdata(request):
    categories = Category.objects.all()
    chart_data = []

    for category in categories:
        books_in_category = Book.objects.filter(category=category)
        total_expense = sum(book.distribution_expense for book in books_in_category)
        chart_data.append({'category': category.name, 'total_expense': total_expense})

    return JsonResponse(chart_data, safe=False)




class SearchView(View):
    template_name = 'search_results.html'
    items_per_page = 10  # Set the number of items per page

    def get(self, request):
        query = request.GET.get('q')
        results = None
        result_count = 0  # Initialize the result count to 0

        if query is not None and query.strip() != "":
            # Use Q objects to search all relevant fields in the Book model
            results = Book.objects.filter(
                Q(title__icontains=query) |  # Search title
                Q(authors__icontains=query) |  # Search authors
                Q(publisher__icontains=query) |  # Search publisher
                Q(category__name__icontains=query) |  # Search category name
                Q(storeId__icontains=query)  # Search by storeId
            ).distinct()

            result_count = results.count()  # Calculate the result count

            paginator = Paginator(results, self.items_per_page)  # Create a paginator
            page = request.GET.get('page')  # Get the current page number

            try:
                results = paginator.page(page)  # Get the current page
            except Exception:
                results = paginator.page(1)  # Display the first page if the requested page is invalid

        return render(request, self.template_name, {'results': results, 'query': query, 'result_count': result_count})

