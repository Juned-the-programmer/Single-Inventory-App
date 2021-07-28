from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE , related_name="profile")
    phone_no = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    #Address
    Address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50) 
    pincode = models.CharField(max_length=50)
    #Bank Detail
    GSTNO = models.CharField(max_length=50)
    Bank_name = models.CharField(max_length=50)
    Bank_AC = models.CharField(max_length=50)
    IFSC_Code = models.CharField(max_length=50)
    Branch_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

def create_profile_estimate(sender,instance,created,**Kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile_estimate,sender=User)
