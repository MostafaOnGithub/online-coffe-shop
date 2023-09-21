from django.shortcuts import render ,get_object_or_404
from .models import Product
def products(request) :
    pro = Product.objects.all()
    name = None
    desc = None
    pricefrom = None
    priceto = None
    cs = None
    if 'cs' in request.GET:
        cs = request.GET['cs']
        if not cs :
            cs = 'off'
    if 'searchname' in request.GET:
        name = request.GET['searchname']
        if name :
            if cs == 'on':
                pro = pro.filter(name__contains= name )    
            else:
                pro = pro.filter(name__icontains= name )
    if 'searchdesc' in request.GET:
        desc = request.GET['searchdesc']
        if desc :
            if cs == 'on':
                pro = pro.filter(description__contains= desc )    
            else:
                pro = pro.filter(description__icontains= desc )
            
    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        pricefrom = request.GET['searchpricefrom']
        priceto = request.GET['searchpriceto']
        if pricefrom and priceto:
            if pricefrom.isdigit() and priceto.isdigit():
                pro = pro.filter(price__gte=pricefrom)
                pro = pro.filter(price__lte =priceto)
    
    context = {
       'product': pro,
    }
    return render(request,'products/products.html',context)
def product(request , pro_id) :
    context = {
        'pro':get_object_or_404(Product,pk = pro_id)
    }
    return render(request,"products/product.html",context)
def search(request):
    return render(request,"products/search.html")

# Create your views here.
