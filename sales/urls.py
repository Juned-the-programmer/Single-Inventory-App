from django.urls import path
from . import views

urlpatterns = [
    path('addsale/',views.addsale,name="addsale"),
    path('viewsale/',views.viewsale,name="viewsale"),
    path('updatesale/<pk>',views.updatesale,name="updatesale"),
    path('saleinvoice/<pk>',views.saleinvoice,name="saleinvoice"),
    #Ajax Call for Estimate Sale Start here
    path('estimatesalec/',views.estimatesalec,name="estimatesalec"),
    path('sellingprice_previous_discount_estimate/',views.sellingprice_previous_discount_estimate,name="sellingprice_previous_discount_estimate"),
    path('customerdue_estimate/',views.customerdue_estimate,name="customerdue_estimate"),
    path('product_data_estimate/',views.product_data_estimate,name="product_data_estimate"),
    path('selected_product/',views.selected_product, name="selected_product"),
    # Ajax Call for GST Sale Start here
    path('gstsalec/',views.gstsalec,name="gstsalec"),
    path('product_data_gst/',views.product_data_gst,name="product_data_gst"),
    path('getproducts_gst_sale/',views.getproducts_gst_sale,name="getproducts_gst_sale"),
    path('customer_state_gst/',views.customer_state_gst,name="customer_state_gst"),
    path('check_stock_gst/',views.check_stock_gst,name="check_stock_gst"),
    path('sellingprice_gst/',views.sellingprice_gst,name="sellingprice_gst"),
    path('ownerstate_gst_sale/',views.ownerstate_gst_sale,name="ownerstate_gst_sale"),
    path('stock_data_gst/',views.stock_data_gst,name="stock_data_gst"),
]
