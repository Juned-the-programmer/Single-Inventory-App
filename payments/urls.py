from django.urls import path
from . import views

urlpatterns = [
    path('supplierpayment/',views.supplierpayment,name="supplierpayment"),
    path('customerpayment/',views.customerpayment,name="customerpayment"),
    path('supplier_dueamount/',views.supplier_dueamount,name="supplier_dueamount"),
    path('customer_dueamount/',views.customer_dueamount,name="customer_dueamount"),
]
