from django.shortcuts import render
from library.models import Books, Category

def home(request, category_slug=None):
     data= Books.objects.all()

     if category_slug is not None:
          category = Category.objects.get(slug= category_slug)
          data = Books.objects.filter(category= category)
     
     categories = Category.objects.all()
     return render(request, 'home.html', {'data': data, 'category': categories})




     