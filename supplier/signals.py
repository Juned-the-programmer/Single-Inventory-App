from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# Signals to create a records in the supplier account model
''' We will create the another raw in the another model for that supplier to maintain the account for that supplier '''

# To create a record for estiamte supplier
@receiver(post_save, sender=Supplier_estimate)
def create_supplier_account_estimate(sender,instance,created,**kwargs):
    if created:
        supplieraccount_estimate.objects.create(supplier_name=instance)

# To create a record for GST supplier.
@receiver(post_save, sender=Supplier_gst)
def create_supplier_account_gst(sender,instance,created,**kwargs):
    if created:
        supplieraccount_gst.objects.create(supplier_name=instance)
        
# post_save we will create a record on the creation of supplier.
post_save.connect(create_supplier_account_estimate,sender=Supplier_estimate)
post_save.connect(create_supplier_account_gst,sender=Supplier_gst)