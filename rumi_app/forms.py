from django.forms import ModelForm, ModelChoiceField, DateInput, TextInput, Select, NumberInput
from .models import Category, Book

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['storeId', 'title', 'subtitle', 'authors', 'publisher', 'published_date', 'category', 'distribution_expense']
        widgets = {
            'published_date': DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['category'] = ModelChoiceField(queryset=Category.objects.all())

    def clean_subtitle(self):
        subtitle = self.cleaned_data.get('subtitle')
        if not subtitle:
            return None  # Convert an empty string to None
        return subtitle

