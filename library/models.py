from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
 
# Create your models here.
 
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Books(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/',blank=True, null= True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="books")
     
    
    def __str__(self):
        return self.title
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def borrow_book(self):
        profile = self.user.userprofile
        if profile.balance >= self.book.borrowing_price:
            profile.balance -= self.book.borrowing_price
            profile.save()
            send_mail('Book Borrowed', f'You borrowed {self.book.title}.', 'library@example.com', [self.user.email])
        else:
            raise ValueError("Insufficient balance")

    def return_book(self):
        if not self.returned:
            self.returned = True
            self.save()
            profile = self.user.userprofile
            profile.balance += self.book.borrowing_price
            profile.save()
            send_mail('Book Returned', f'You returned {self.book.title}.', 'library@example.com', [self.user.email])

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, related_name="reviews", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"