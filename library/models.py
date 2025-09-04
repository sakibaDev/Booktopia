from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=120)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=80, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Member(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, related_name='borrows', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='borrows', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-borrow_date']
