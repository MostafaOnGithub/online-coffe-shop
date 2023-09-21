from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Product,through="OrderDetails")
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self) -> str:
        return f"User:{self.user.username} , Order id: {str(self.id)}"
    
class OrderDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=6 ,decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"User:{self.order.user.username} , Product:{self.product.name} , Order Id {str(self.order.id)}"

class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=20)
    card_number = CardNumberField()
    expire_number = CardExpiryField()
    security_code = SecurityCodeField()
