from django.db import models
from supplier.models import *

# Create your models here.
class Estimate_purchase_bill_number(models.Model):
    last_bill_number = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.last_bill_number)

class Gst_purchase_bill_number(models.Model):
    last_bill_number = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.last_bill_number)

class Estimate_Purchase(models.Model):
    Bill_no = models.IntegerField()
    supplier = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    Total_amount = models.FloatField()
    Due_amount = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.Bill_no)

    class Meta:
        indexes = [models.Index(fields=('Bill_no' , 'id' , 'supplier'))]

class estimatepurchase_Product(models.Model):
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
        indexes = [models.Index(fields=('Bill_no' , 'id' , 'product_name'))]

class GST_Purchase(models.Model):
    Bill_no = models.IntegerField()
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
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

class gstpurchase_Product(models.Model):
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
