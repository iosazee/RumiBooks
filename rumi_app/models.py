from django.db import models

# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    storeId = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    subtitle = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    authors = models.CharField(max_length=100, db_index=True)
    publisher = models.CharField(max_length=100, db_index=True)
    published_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distribution_expense = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.title