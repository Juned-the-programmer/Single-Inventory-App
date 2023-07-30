from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(customerpay_estimate)
admin.site.register(customerpay_gst)
admin.site.register(supplierpay_estimate)
admin.site.register(supplierpay_gst)