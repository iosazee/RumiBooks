from django.core.management.base import BaseCommand
import pandas as pd
from rumi_app.models import Book, Category
from django.core.exceptions import ValidationError
from dateutil.parser import parse
from django.db.models import Q  # Import Q for case-insensitive queries

class Command(BaseCommand):
    help = 'Import data from an Excel spreadsheet into the database'

    def handle(self, *args, **options):
        excel_file = './Copy of Books Distribution Expenses.xlsx'

        try:
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                category_name = row['category']
                # Check if a category with a case-insensitive name already exists
                category = Category.objects.filter(
                    Q(name__iexact=category_name)
                ).first()

                if not category:
                    # If not found, create a new category with the given name
                    category = Category(name=category_name)
                    category.save()

                # Convert the 'published_date' format using dateutil
                raw_date = str(row['published_date'])
                try:
                    # Use dateutil to parse the date
                    published_date = parse(raw_date).date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'Invalid date format for {row["title"]}'))
                    continue

                # Check if a book with the same storeId already exists
                existing_book = Book.objects.filter(storeId=row['id']).first()
                if existing_book:
                    # Update the existing book with the information from the new row
                    existing_book.title = row['title']
                    existing_book.subtitle = row['subtitle']
                    existing_book.authors = row['authors']
                    existing_book.publisher = row['publisher']
                    existing_book.published_date = published_date
                    existing_book.category = category
                    existing_book.distribution_expense = row['distribution_expense']
                    existing_book.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated {existing_book.title}'))
                else:
                    # Create a new book if it doesn't exist
                    book = Book(
                        storeId=row['id'],
                        title=row['title'],
                        subtitle=row['subtitle'],
                        authors=row['authors'],
                        publisher=row['publisher'],
                        published_date=published_date,
                        category=category,
                        distribution_expense=row['distribution_expense']
                    )

                    book.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully imported {book.title}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

