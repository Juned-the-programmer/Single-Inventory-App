from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer_estimate)
admin.site.register(customeraccount_estimate)
admin.site.register(customerpay_estimate)
#GST
admin.site.register(Customer_gst)
admin.site.register(customeraccount_gst)

admin.site.register(Supplier_estimate)
admin.site.register(supplieraccount_estimate)
admin.site.register(supplierpay_estimate)
#GST
admin.site.register(Supplier_gst)
admin.site.register(supplieraccount_gst)

admin.site.register(Product_estimate)
admin.site.register(Product_gst)
admin.site.register(Stock_estimate)
admin.site.register(Stock_gst)

admin.site.register(Estimate_Purchase)
admin.site.register(estimatepurchase_Product)
admin.site.register(GST_Purchase)
admin.site.register(gstpurchase_Product)

admin.site.register(Estimate_sales)
admin.site.register(estimatesales_Product)
admin.site.register(gstsale)
admin.site.register(gstsales_Product)

admin.site.register(dailyincome_estimate)
admin.site.register(dailyincome_gst)
admin.site.register(dailyexpense_estimate)
admin.site.register(dailyexpense_gst)
admin.site.register(category_estimate)
admin.site.register(category_gst)