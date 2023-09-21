from django.shortcuts import render,redirect
from django.contrib import messages
from products.models import Product
from .models import Order,OrderDetails,Payment
from django.utils import timezone


def add_to_cart(request):
    if "pro_id" in request.GET and "QTY" in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET["pro_id"]
        qty = request.GET["QTY"]
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect("home page")
        pro = Product.objects.get(id=pro_id)
        order = Order.objects.all().filter(user=request.user,is_finished=False)
        if order:
            old_order = Order.objects.get(user = request.user,is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order,product=pro).exists():
                orderdetails = OrderDetails.objects.get(order=old_order,product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else:
                orderdetails = OrderDetails.objects.create(product = pro , order = old_order ,price = pro.price,quantity = qty)
            messages.success(request,"Added To Cart")
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            orderdetails = OrderDetails.objects.create(product=pro,price=pro.price,order=new_order,quantity = qty)
            messages.success(request,"Added To Cart")
            
            
        return redirect("/products/" + request.GET["pro_id"])
    else:
        if "pro_id" in request.GET:
            messages.error(request,"You Must Be Logged In First")
            return redirect("/products/" + request.GET["pro_id"])

        else:
            return redirect("products page")


def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order = Order.objects.get(user = request.user,is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            total = 0
            for o in orderdetails:
                total += o.price * o.quantity
            context = {
                "order":order,
                "orderdetails":orderdetails,
                "total":total
            }
    return render(request,"orders/cart.html",context)


def remove_from_cart(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()
    return redirect("cart")


def AddQuantity(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.quantity += 1
        orderdetails.save()
    return redirect("cart")


def SupQuantity(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()
    return redirect("cart")


def payment_page(request):
    context = None
    shipaddress = None
    shipphone = None
    securitycode = None
    expire = None
    cardnumber = None
    is_added = None
    if request.method == 'POST' and "btnpay" in request.POST and "shipaddress" in request.POST and "shipphone" in request.POST and "cardnumber" in request.POST and "expire" in request.POST and "securitycode" in request.POST:
        shipaddress = request.POST["shipaddress"]
        securitycode = request.POST["securitycode"]
        shipphone = request.POST["shipphone"]
        expire = request.POST["expire"]
        cardnumber = request.POST["cardnumber"]
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order = Order.objects.get(user = request.user,is_finished=False)
                payment = Payment(security_code = securitycode ,shipment_address=shipaddress ,card_number = cardnumber,shipment_phone=shipphone,order = order,expire_number=expire)
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request,"Your Order Is Finished")
        context = {
            'shipaddress':shipaddress,
            'shipnumber':shipphone,
            'securitycode':securitycode,
            'expire':expire,
            'cardnumber':cardnumber,
            'is_added':is_added,
        }
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order = Order.objects.get(user = request.user,is_finished=False)
                orderdetails=OrderDetails.objects.all().filter(order=order)
                total = 0
                for o in orderdetails:
                    total += o.price * o.quantity
                context = {
                    "order":order,
                    "orderdetails":orderdetails,
                    "total":total
                }
    return render(request,"orders/payment.html",context)


def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id =x.id)
                orderdetails=OrderDetails.objects.all().filter(order=order)
                total = 0
                for o in orderdetails:
                    total += o.price * o.quantity
                x.total = total
                x.items_count = orderdetails.count
                
    context = {
        "all_orders":all_orders,
    }
    return render(request,"orders/showorders.html",context)
