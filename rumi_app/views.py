from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Book
from .forms import CategoryForm, BookForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy

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