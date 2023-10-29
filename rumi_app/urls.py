from django.urls import path
from .views import home, privacy, CategoryListView, CategoryCreateView, CategoryUpdateView, CustomCategoryDeleteView

urlpatterns = [
    path('', home, name="home"),
    path('privacy/', privacy, name="privacy"),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CustomCategoryDeleteView.as_view(), name='category_delete'),
]