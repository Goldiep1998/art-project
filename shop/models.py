from django.db import models
from django.contrib.auth.models import User
from sell.models import Image

# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    finalized = models.BooleanField(default=False)

def __str__(self):
    return self.id
    

class OrderItems(models.Model):
    item = models.OneToOneField(Image, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')


def __str__(self):
    return self.item