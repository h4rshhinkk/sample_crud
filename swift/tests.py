from django.test import TestCase

# Create your tests here
a = {'a':'a','b':'b'}
a['a'] = 'new_value' 
print(a)


class City(models.Model):
    name = models.CharField(max_length=100)

class Author(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Store(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    # Without optimization
stores = Store.objects.all()
for store in stores:
    for book in store.books.all():  # Query for each store
        print(store.name, book.title, book.author.name, book.author.city.name)  # Query for each book

# With select_related and prefetch_related
stores = Store.objects.prefetch_related('books__author__city').all()
for store in stores:
    for book in store.books.all():  # Single query for books and their related authors and cities
        print(store.name, book.title, book.author.name, book.author.city.name)