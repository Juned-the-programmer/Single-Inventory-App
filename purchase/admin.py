from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Estimate_Purchase)
admin.site.register(estimatepurchase_Product)
admin.site.register(GST_Purchase)
admin.site.register(gstpurchase_Product)
admin.site.register(Estimate_purchase_bill_number)
admin.site.register(Gst_purchase_bill_number)