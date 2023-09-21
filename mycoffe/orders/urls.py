from django.urls import path
from . import views

urlpatterns =[
    path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path("cart",views.cart,name="cart"),
    path("remove_from_cart/<int:orderdetails_id>",views.remove_from_cart,name="remove_from_cart"),
    path("addqty/<int:orderdetails_id>",views.AddQuantity,name="addqty"),
    path("subqty/<int:orderdetails_id>",views.SupQuantity,name="subqty"),
    path("payment",views.payment_page,name="payment"),
    path("showorders",views.show_orders,name="showorders"),
]
