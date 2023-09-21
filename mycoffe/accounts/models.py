from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    product_fav = models.ManyToManyField(Product)
    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username


# Create your models here.
