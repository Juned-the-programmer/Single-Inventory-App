from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(dailyincome_estimate)
admin.site.register(dailyincome_gst)
admin.site.register(dailyexpense_estimate)
admin.site.register(dailyexpense_gst)
admin.site.register(category_estimate)
admin.site.register(category_gst)