from django.urls import path
from .views import home, privacy, CategoryListView, CategoryCreateView, CategoryUpdateView, CustomCategoryDeleteView, BookListView, BookDetailView, BookCreateView, BookUpdateView, CustomBookDeleteView, expense_report, expense_chartdata, SearchView

urlpatterns = [
    path('', home, name="home"),
    path('privacy/', privacy, name="privacy"),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CustomCategoryDeleteView.as_view(), name='category_delete'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', CustomBookDeleteView.as_view(), name='book_delete'),
    path('report/book_expense/', expense_report, name='expense_report'),
    path('expense-chartdata/', expense_chartdata, name='expense_chartdata'),
    path('search/', SearchView.as_view(), name='search'),
]