from django.db import models
import uuid
from django.db.models.signals import post_save

# Create your models here.
class Supplier_estimate(models.Model):
    supplier_id = models.CharField(max_length=10, null=True, blank=True)
    fullname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.fullname

    class Meta:
        indexes = [models.Index(fields=['id' , 'fullname'])]

class supplieraccount_estimate(models.Model):
    supplier_name = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    amount = models.FloatField(default=0,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.supplier_name.fullname)
    
    class Meta:
        indexes = [models.Index(fields=['supplier_name' , 'id'])]
        
class Supplier_gst(models.Model):
    supplierid = models.CharField(max_length=10, null=True, blank=True)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contactno = models.CharField(max_length=50)
    gst = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.fullname

class supplieraccount_gst(models.Model):
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.supplier_name.fullname)

def create_supplier_account_estimate(sender,instance,created,**kwargs):
    if created:
        supplieraccount_estimate.objects.create(supplier_name=instance)

def create_supplier_account_gst(sender,instance,created,**kwargs):
    if created:
        supplieraccount_gst.objects.create(supplier_name=instance)
        
post_save.connect(create_supplier_account_estimate,sender=Supplier_estimate)
post_save.connect(create_supplier_account_gst,sender=Supplier_gst)