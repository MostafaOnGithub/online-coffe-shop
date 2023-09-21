from django.urls import path
from . import views

urlpatterns = [

    path('signin',views.signin , name = 'sign in page'),
    path("signup",views.signup , name = "sign up page"),
    path("profile",views.profile,name = "profile page"),
    path("logout",views.logout,name="logout page"),
    path("product_favourate/<int:pro_id>",views.product_favourate,name = "product_favourate"),
    path("show_product_favourate",views.show_product_favourate,name="show_product_favourate"),
]