from django.urls import path
from . import views

urlpatterns = [
    path('addsale/',views.addsale,name="addsale"),
    path('viewsale/',views.viewsale,name="viewsale"),
    path('updatesale/<pk>',views.updatesale,name="updatesale"),
    path('saleinvoice/<pk>',views.saleinvoice,name="saleinvoice"),
    #Ajax Call for Estimate Sale Start here
    path('customerdue_estimate/',views.customerdue_estimate,name="customerdue_estimate"),
    path('product_data_estimate/',views.product_data_estimate,name="product_data_estimate"),
    path('selected_product/',views.selected_product, name="selected_product"),
    # Ajax Call for GST Sale Start here
    path('customer_state_gst/',views.customer_state_gst,name="customer_state_gst")
]
