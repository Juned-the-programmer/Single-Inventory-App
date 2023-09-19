from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product_estimate)
admin.site.register(Product_gst)
admin.site.register(Stock_estimate)
admin.site.register(Stock_gst)
admin.site.register(Product_type)
admin.site.register(product_required_to_manufacture)
admin.site.register(product_category)