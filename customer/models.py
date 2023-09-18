from django.db import models
import uuid
from django.core.validators import RegexValidator

# Create your models here.
class Customer_estimate(models.Model):
    phone_regex = RegexValidator(
        regex=r'^[789]\d{9}$',
        message="Invalid phone number"
    )
    customer_id = models.CharField(max_length=10, null=True, blank=True)
    fullname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=10, validators=[phone_regex], null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.fullname

    class Meta:
        indexes = [models.Index(fields = [ 'id' , 'fullname'])]

class customeraccount_estimate(models.Model):
    customer_name = models.OneToOneField(Customer_estimate,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)

    class Meta:
        indexes = [models.Index(fields=['id' , 'customer_name'])]
        
class Customer_gst(models.Model):
    customerid = models.CharField(max_length=10, null=True, blank=True)
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
    customer_name = models.OneToOneField(Customer_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return str(self.customer_name.fullname)