from django.db import models
import uuid
import datetime
from django.contrib.auth.models import User


# Create your models here.


class products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    img = models.FileField(upload_to='Thumbnail',null=False)
    title = models.CharField(max_length=70,null=False)
    desc = models.TextField(max_length=500,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class addcart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cart_items',null=True)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price
        
    def __str__(self):
        return f"{self.product.title}"

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.title} in Order {self.order.order_id}"

