from django.db import models
from customer.models import *
from supplier.models import *

# Create your models here.
class customerpay_estimate(models.Model):
    customer_name = models.ForeignKey(Customer_estimate , on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    round_off = models.FloatField()
    date = models.DateField(auto_now_add=True)
    Description = models.CharField(max_length=100,blank=True,null=True,default="Cash on Hand")
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)

    class Meta:
        indexes = [models.Index(fields=['customer_name' , 'id'])]

class customerpay_gst(models.Model):
    customer_name = models.ForeignKey(Customer_gst , on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    round_off = models.FloatField()
    date = models.DateField(auto_now_add=True)
    Description = models.CharField(max_length=100,blank=True,null=True,default="Cash on Hand")
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)

class supplierpay_estimate(models.Model):
    supplier_name = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    round_off = models.FloatField()
    date = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.supplier_name.fullname)

    class Meta:
        indexes = [models.Index(fields=['supplier_name' , 'id'])]

class supplierpay_gst(models.Model):
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    round_off = models.FloatField()
    date = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.supplier_name.fullname)