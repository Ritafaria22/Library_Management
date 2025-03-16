from django.urls import path
from . import views
from .views import DepositMoneyView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    path('history/', views.borrowing_history, name='borrowing_history'),
     path('check-balance/', views.check_balance, name='check_balance'),
    path('logout/', views.user_logout, name='logout'),
]