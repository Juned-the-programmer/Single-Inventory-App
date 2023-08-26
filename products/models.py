from django.db import models
import uuid
from supplier.models import *

# Create your models here.
class Product_estimate(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_estimate , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_name

    class Meta:
        indexes = [models.Index(fields=('product_name' , 'id' , 'supplier'))]

class Stock_estimate(models.Model):
    product = models.OneToOneField(Product_estimate,on_delete=models.CASCADE)    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.product.product_name)

    class Meta:
        indexes = [models.Index(fields=('product' , 'id'))]

class Product_gst(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_gst , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_name

class Stock_gst(models.Model):
    product = models.OneToOneField(Product_gst,on_delete=models.CASCADE)    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.product.product_name)