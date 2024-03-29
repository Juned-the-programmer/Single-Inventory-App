from django.db import models
import uuid
from supplier.models import *

# Create your models here.
class product_category(models.Model):
    product_category = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_category

class product_category_gst(models.Model):
    product_category = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_category

class Product_type(models.Model):
    product_type = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_type

    @classmethod
    def create_initial_data(cls):
        cls.objects.create(product_type='Retail', id=uuid.uuid4())
        cls.objects.create(product_type='Manufacture', id=uuid.uuid4())

class product_type_gst(models.Model):
    product_type = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_type

    @classmethod
    def create_intial_data(cls):
        cls.objects.create(product_type='Retail', id=uuid.uuid4())
        cls.objects.create(product_type='Manufacture', id=uuid.uuid4())

class Product_estimate(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.ForeignKey(product_category, null=True, blank=True, on_delete=models.SET_NULL)
    product_type = models.ForeignKey(Product_type, null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    purchase_price = models.FloatField(null=True, blank=True, default=0)
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_estimate , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_name

    class Meta:
        indexes = [models.Index(fields=('id' , 'supplier'))]

class Stock_estimate(models.Model):
    product = models.OneToOneField(Product_estimate,on_delete=models.CASCADE, related_name="stock_estimate")    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.product.product_name)

    class Meta:
        indexes = [models.Index(fields=('product' , 'id'))]

class Product_gst(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.ForeignKey(product_category_gst, null=True, blank=True, on_delete=models.SET_NULL)
    product_type = models.ForeignKey(product_type_gst, null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    purchase_price = models.FloatField(null=True, blank=True, default=0)
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_gst , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.product_name

    class Meta:
        indexes = [models.Index(fields=('id', 'supplier'))]

class Stock_gst(models.Model):
    product = models.OneToOneField(Product_gst,on_delete=models.CASCADE, related_name="stock_gst")    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.product.product_name)

    class Meta:
        indexes = [models.Index(fields=('product' , 'id'))]

class product_required_to_manufacture(models.Model):
    manufacture_product = models.ForeignKey(Product_estimate, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufactured_products')
    desciption = models.CharField(max_length=500, null=True, blank=True)
    required_products = models.ManyToManyField(Product_estimate , blank=True, symmetrical=False, related_name='required_products_for_manufacture')

    def __str__(self):
        return self.manufacture_product.product_name

class product_required_to_manufacture_gst(models.Model):
    manufacture_product = models.ForeignKey(Product_gst, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufactured_products_gst')
    desciption = models.CharField(max_length=500, null=True, blank=True)
    required_products = models.ManyToManyField(Product_gst , blank=True, symmetrical=False, related_name='required_products_for_manufacture_gst')

    def __str__(self):
        return self.manufacture_product.product_name