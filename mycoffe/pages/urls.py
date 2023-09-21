from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage , name = 'home page'),
    path("about",views.about , name = "about page"),
    path('coffe',views.coffe ,name = "coffe page"),
]