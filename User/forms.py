from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))
    class Meta:
        model=User
        fields= ['username','first_name', 'last_name', 'email']

class DepositForm(forms.Form):
        amount = forms.DecimalField(
            max_digits=10,
            decimal_places=2,
            min_value=0.01,
            label='Deposit Amount',
            widget=forms.NumberInput(attrs={'placeholder': 'Enter amount to deposit'})
        )