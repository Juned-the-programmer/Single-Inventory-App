from django.db import models
from django.db.models.signals import post_save
import uuid
from customer.models import *
from supplier.models import *
from products.models import *

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

class Estimate_sales(models.Model):
    Bill_no = models.IntegerField()
    customer = models.ForeignKey(Customer_estimate,on_delete=models.CASCADE)
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
    # date = models.DateField(auto_now_add=True)
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

class dailyincome_estimate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.name

class dailyincome_gst(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.name

class dailyexpense_estimate(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category

class dailyexpense_gst(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category

class category_estimate(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category_name

class category_gst(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category_name