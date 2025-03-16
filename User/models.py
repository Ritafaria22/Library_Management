from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.db import models
from django.core.mail import send_mail
 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.user.username
    
