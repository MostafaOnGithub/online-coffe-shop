from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import userprofile
import re
from django.contrib import auth
from products.models import Product


def signin(request) :
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username,password=password)
        if user is not None :
            if  "remember" not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
        else:
            messages.error(request,"Username or password is Incorrect")
        return render(request,'accounts/SignIn.html')
    else :
        return render(request,'accounts/SignIn.html')


def signup(request) :
    if request.method == "POST":
        fname = None
        lname = None
        address = None
        address2 = None
        state = None
        city = None
        email = None
        username = None
        password = None
        zip = None
        terms = None
        is_added = None

        if "fname" in request.POST:fname = request.POST["fname"]
        else : messages.error(request, "Enter Your First Name")
        if "lname" in request.POST:lname = request.POST["lname"]
        else : messages.error(request, "Enter Your Last Name")
        if "address" in request.POST:address = request.POST["address"]
        else : messages.error(request, "Enter Your Address")
        if "address2" in request.POST:address2 = request.POST["address2"]
        else : messages.error(request, "Enter Your Second Address")
        if "city" in request.POST: city = request.POST["city"]
        else : messages.error(request, "Enter Your City")
        if "state" in request.POST:state = request.POST["state"]
        else : messages.error(request, "Enter Your State")
        if "zip" in request.POST:zip = request.POST["zip"]
        else : messages.error(request, "Enter Your Zip Code")
        if "email" in request.POST:email = request.POST["email"]
        else : messages.error(request, "Enter Your Email")
        if "username" in request.POST:username = request.POST["username"]
        else : messages.error(request, "Enter Your UserName")
        if "password" in request.POST:password = request.POST["password"]
        else : messages.error(request, "Enter Your password")
        if "terms" in request.POST:terms = request.POST["terms"]

        if fname and lname and address and address2 and city and state and zip and email and username and password:
            if terms == "on":
                if User.objects.filter(username = username).exists():
                    messages.error(request,"This Username is Already taken")
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request,"This Email Is Already Taken")
                    else :
                        patt = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                        if re.match(patt,email):
                            user = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            Userprofile = userprofile(user=user,address= address,address2= address2,state=state,city=city,zip=zip)
                            Userprofile.save()
                            messages.success(request,"account Has Been Created Succesfully")
                            is_added = True
                        else:
                            messages.error(request,"Invalid Email")
                        
            else: messages.error(request,"You must Accept the Terms of Policy")
        else : messages.error(request, "check Empty Fields")

        return render(request , "accounts/signup.html",{
            "fname" : fname,
            "lname":lname,
            "address":address,
            "address2":address2,
            "city":city,
            "state":state,
            "username":username,
            "password":password,
            "zip":zip,
            "email":email,
            "is_added":is_added,


        })
    else :
        return render(request , "accounts/signup.html")




def profile(request) :
    if request.method == "POST":
        if request.user is not None and request.user.id != None:
            Userprofile = userprofile.objects.get(user = request.user)
            if  request.POST["fname"] and request.POST["lname"] and request.POST["city"] and request.POST["state"] and request.POST["zip"] and request.POST["address"] and request.POST["address2"] and request.POST["email"] and request.POST["username"] and request.POST["password"]:
                request.user.first_name = request.POST["fname"]
                request.user.last_name = request.POST["lname"]
                Userprofile.address = request.POST["address"]
                Userprofile.address2 = request.POST["address2"]
                Userprofile.city = request.POST["city"]
                Userprofile.state = request.POST['state']
                Userprofile.zip = request.POST["zip"]
                if not request.POST["password"].startswith("pbkdf2_sha256$"):
                    request.user.set_password(request.POST["password"])
                request.user.save()
                Userprofile.save()
                auth.login(request,request.user)
                messages.success(request,"Your Date Has Been Changed")
            else :
                messages.error(request,"Check Empty Values")

        return redirect('profile page')
    else :
        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                Userprofile = userprofile.objects.get(user=request.user)
                context = {
                    "fname":request.user.first_name,
                    "lname":request.user.last_name,
                    "email":request.user.email,
                    "username":request.user.username,
                    "password":request.user.password,
                    "address":Userprofile.address,
                    "address2":Userprofile.address2,
                    "city":Userprofile.city,
                    "state":Userprofile.state,
                    "zip":Userprofile.zip
                }

            
            return render(request ,"accounts/profile.html",context)
        else : 
            return redirect("profile page")
        



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("home page")



def product_favourate(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous :
        pro_fav = Product.objects.get(pk = pro_id)
        if userprofile.objects.filter(user= request.user,product_fav=pro_fav).exists():
            messages.info(request,"Products Is Already favourate")
        else:
            Userprofile =userprofile.objects.get(user=request.user)
            Userprofile.product_fav.add(pro_fav)
            messages.success(request,"product have been added to the favourates list")

        
    else: messages.error(request,"you must be logged in first")
    return redirect("/products/" + str(pro_id))


def show_product_favourate(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous :
        userinfo = userprofile.objects.get(user=request.user)
        pro =userinfo.product_fav.all()
        context = {
            "product":pro
        }
    return render(request,"products/products.html",context)
