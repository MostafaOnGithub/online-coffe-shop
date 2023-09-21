from django.urls import path
from . import views

urlpatterns = [
    path("",views.products,name = "products page"),
    path("<int:pro_id>",views.product,name = "product page"),
    path("search",views.search,name = 'search page'),
]