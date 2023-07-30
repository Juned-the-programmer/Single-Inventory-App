from django.urls import path
from . import views

urlpatterns = [
    path('supplierpayment/',views.supplierpayment,name="supplierpayment"),
    path('customerpayment/',views.customerpayment,name="customerpayment"),
    path('supplier_dueamount_estimate/',views.supplier_dueamount_estimate,name="supplier_dueamount_estimate"),
    path('customer_dueamount_estimate/',views.customer_dueamount_estimate,name="customer_dueamount_estimate"),
    path('customer_dueamount_gst/',views.customer_dueamount_gst,name="customer_dueamount_gst"),
    path('supplier_dueamount_gst/',views.supplier_dueamount_gst,name="supplier_dueamount_gst"),
]
