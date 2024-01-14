from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from dashboard.models import *

# Signals to add the customeraccount record while adding customer data.
''' So here the thing is that if we are adding new customer then it will generate one another row for that 
customer in customerAccount model to maintain the account for that customer '''
@receiver(post_save, sender=Customer_estimate)
def create_customer_account_estimate(sender,instance,created,**kwargs):
    if created:
        customeraccount_estimate.objects.create(customer_name=instance)
        dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
        dashboard_data.total_customer_count += 1
        dashboard_data.save()

@receiver(post_save, sender=Customer_gst)
def create_customer_account_gst(sender,instance,created,**kwargs):
    if created:
        customeraccount_gst.objects.create(customer_name=instance)
        
post_save.connect(create_customer_account_estimate,sender=Customer_estimate)
post_save.connect(create_customer_account_gst,sender=Customer_gst)