from django.urls import path
from . import views

urlpatterns = [
    path('booklist', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('book/<int:book_id>/', views.book_details, name='book_detail'), 
      
     
]