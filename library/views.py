from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Books, BorrowedBook
from .forms import BookForm
from .models import Books, BorrowedBook, Review, Category
from django.contrib import messages
from User.models import UserProfile 


# Create your views here.
@login_required
def add_book(request):
    if not request.user.is_staff:  # Only admin users can add books
        return redirect('home')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required
def book_list(request,category_slug=None):
    categories = Category.objects.all()
    books = Books.objects.all()
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=selected_category)

    context = {
        'categories': categories,
        'books': books,
        'selected_category': selected_category.slug if selected_category else None
    }
    return render(request, 'book_list.html', {'books': books})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    profile = UserProfile.objects.get(user=request.user)

    if profile.balance >= book.borrowing_price:
        # Create a borrowed book record
        borrowed_book = BorrowedBook.objects.create(user=request.user, book=book)
        profile.balance -= book.borrowing_price
        profile.save()
        return redirect('home')  # Redirect after borrowing
    else:
        return render(request, 'insufficient_balance.html') 

@login_required
def return_book(request, borrow_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrow_id)
    
    # Check if the borrowed book belongs to the logged-in user and is not already returned
    if borrowed_book.user == request.user and not borrowed_book.returned:
        borrowed_book.returned = True
        borrowed_book.save()

        # Refund the borrowing price to the user's balance
        profile = UserProfile.objects.get(user=request.user)
        profile.balance += borrowed_book.book.borrowing_price
        profile.save()

        messages.success(request, 'Book returned successfully! Your balance has been updated.')
        return redirect('borrowing_history')  # Redirect to the borrowing history page
    else:
        messages.error(request, 'You cannot return this book.')
        return redirect('borrowing_history')   


@login_required
def book_details(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    reviews = Review.objects.filter(book=book)

     
    if request.method == 'POST':
        # Handle the review submission
        review_text = request.POST.get('review')
        if request.user.is_authenticated and review_text:
            Review.objects.create(user=request.user, book=book, text=review_text)

    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

