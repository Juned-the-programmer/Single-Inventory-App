from django.db import models
import uuid
from django.db.models.signals import post_save

# Create your models here.
class Customer_estimate(models.Model):
    fullname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.fullname

    class Meta:
        indexes = [models.Index(fields = [ 'id' , 'fullname'])]

class customeraccount_estimate(models.Model):
    customer_name = models.ForeignKey(Customer_estimate,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)

    class Meta:
        indexes = [models.Index(fields=['id' , 'customer_name'])]
        
class Customer_gst(models.Model):
    customerid = models.IntegerField()
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

class customeraccount_gst(models.Model):
    customer_name = models.ForeignKey(Customer_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)
    
def create_customer_account_estimate(sender,instance,created,**kwargs):
    if created:
        customeraccount_estimate.objects.create(customer_name=instance)

def create_customer_account_gst(sender,instance,created,**kwargs):
    if created:
        customeraccount_gst.objects.create(customer_name=instance)
        
post_save.connect(create_customer_account_estimate,sender=Customer_estimate)
post_save.connect(create_customer_account_gst,sender=Customer_gst)