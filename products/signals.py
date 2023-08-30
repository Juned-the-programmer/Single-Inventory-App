from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from dashboard.models import *

''' To create the stock data when we add the new product details '''
@receiver(post_save, sender=Product_estimate)
def create_stock_estimate(sender,instance,created,**kwargs):
    if created:
        Stock_estimate.objects.create(product=instance)
        dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
        dashboard_data.total_product_count += 1
        dashboard_data.save()

@receiver(post_save, sender=Product_gst)
def create_stock_gst(sender,instance,created,**kwargs):
    if created:
        Stock_gst.objects.create(product=instance)
    
post_save.connect(create_stock_estimate,sender=Product_estimate)
post_save.connect(create_stock_gst,sender=Product_gst)