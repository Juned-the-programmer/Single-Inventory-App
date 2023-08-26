from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Supplier_estimate)
def create_supplier_account_estimate(sender,instance,created,**kwargs):
    if created:
        supplieraccount_estimate.objects.create(supplier_name=instance)

@receiver(post_save, sender=Supplier_gst)
def create_supplier_account_gst(sender,instance,created,**kwargs):
    if created:
        supplieraccount_gst.objects.create(supplier_name=instance)
        
post_save.connect(create_supplier_account_estimate,sender=Supplier_estimate)
post_save.connect(create_supplier_account_gst,sender=Supplier_gst)