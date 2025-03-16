from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from library.models import Books
from django.contrib import messages
from library.models import BorrowedBook
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings 
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django import forms
from .forms import DepositForm 
from django.http import HttpResponse
# Create your views here.

# Function to send confirmation email
def send_confirmation_email(user_email, amount, balance):
    """Send a deposit confirmation email."""
    subject = 'Deposit Confirmation'
    template = "deposit_email.html"
    
    message = render_to_string(template, {
        'amount': amount,
        'balance': balance,
    })

    email = EmailMultiAlternatives(subject, '',  settings.EMAIL_HOST_USER, [user_email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=False)

class DepositMoneyView(LoginRequiredMixin, FormView):
    template_name = 'deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        
        if amount <= 0:
            messages.error(self.request, "Invalid deposit amount.")
            return redirect('deposit')

        profile = UserProfile.objects.get(user=self.request.user)
        profile.balance += amount
        profile.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'${amount:,.2f} deposited successfully!'
        )

        
        send_confirmation_email(self.request.user.email, amount, profile.balance)
        return super().form_valid(form)

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# @login_required            
# def profile(request):
#     data= Books.objects.filter(author=request.user)
#     return render(request, 'profile.html', {'data': data})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
 
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def borrowing_history(request):
    """Show borrowing history of the logged-in user."""
    borrowed_books = BorrowedBook.objects.filter(user=request.user).order_by('-borrowed_date')
    return render(request, 'borrowing_history.html', {'borrowed_books': borrowed_books})

@login_required
def check_balance(request):
    """View to check the user's account balance."""
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'check_balance.html', {'balance': profile.balance})

 