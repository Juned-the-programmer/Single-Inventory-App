from django.db import models
import uuid

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
    supplier_name = models.OneToOneField(Supplier_estimate,on_delete=models.CASCADE)
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
    supplier_name = models.OneToOneField(Supplier_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.supplier_name.fullname)