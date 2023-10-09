from django.db import models
import uuid
from customer.models import *

# Create your models here.
class Estimate_sale_bill_number(models.Model):
    last_bill_number = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.last_bill_number)

class GST_sale_bill_number(models.Model):
    last_bill_number = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self, last_bill_number)

class Estimate_sales(models.Model):
    Bill_no = models.IntegerField()
    customer = models.ForeignKey(Customer_estimate,on_delete=models.CASCADE, related_name="estimate_sales")
    date = models.DateField(auto_now_add=True)
    Total_amount = models.FloatField()
    Due_amount = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.Bill_no)

    class Meta:
        indexes = [models.Index(fields=['Bill_no' , 'customer' , 'id'])]
    
class estimatesales_Product(models.Model):
    Bill_no = models.IntegerField()
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    dis = models.FloatField()
    netrate = models.FloatField()
    total = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.Bill_no)

    class Meta:
        indexes = [models.Index(fields=['Bill_no' , 'id' , 'product_name'])]

class gstsale(models.Model):
    Bill_no = models.IntegerField()
    customer_name =  models.ForeignKey(Customer_gst,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    CGST = models.FloatField()
    SGST = models.FloatField()
    IGST = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.Bill_no)

class gstsales_Product(models.Model):
    Bill_no = models.IntegerField()
    hsncode=models.IntegerField()
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    gstp = models.FloatField()
    gstamt = models.FloatField()
    total = models.FloatField()
    # date = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.Bill_no)