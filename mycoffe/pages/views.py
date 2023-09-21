from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product

def homepage(request) :
    context ={
        'product':Product.objects.all()
    }
    return render(request , 'pages/home.html', context)

def about(request) :
    return render(request , 'pages/about.html')

def coffe(request) :
    return render(request , "pages/coffe.html")

# Create your views here.
