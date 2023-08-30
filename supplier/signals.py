from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from dashboard.models import *

# Signals to create a records in the supplier account model
''' We will create the another raw in the another model for that supplier to maintain the account for that supplier '''

# To create a record for estiamte supplier
@receiver(post_save, sender=Supplier_estimate)
def create_supplier_account_estimate(sender,instance,created,**kwargs):
    if created:
        supplieraccount_estimate.objects.create(supplier_name=instance)
        dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
        dashboard_data.total_supplier_count += 1
        dashboard_data.save()

# To create a record for GST supplier.
@receiver(post_save, sender=Supplier_gst)
def create_supplier_account_gst(sender,instance,created,**kwargs):
    if created:
        supplieraccount_gst.objects.create(supplier_name=instance)
        
# post_save we will create a record on the creation of supplier.
post_save.connect(create_supplier_account_estimate,sender=Supplier_estimate)
post_save.connect(create_supplier_account_gst,sender=Supplier_gst)