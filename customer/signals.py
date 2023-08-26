from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Customer_estimate)
def create_customer_account_estimate(sender,instance,created,**kwargs):
    if created:
        customeraccount_estimate.objects.create(customer_name=instance)

@receiver(post_save, sender=Customer_gst)
def create_customer_account_gst(sender,instance,created,**kwargs):
    if created:
        customeraccount_gst.objects.create(customer_name=instance)
        
post_save.connect(create_customer_account_estimate,sender=Customer_estimate)
post_save.connect(create_customer_account_gst,sender=Customer_gst)