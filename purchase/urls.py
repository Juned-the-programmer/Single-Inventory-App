from django.urls import path
from . import views

urlpatterns = [
    path('addpurchase/',views.addpurchase,name="addpurchase"),
    path('viewpurchase/',views.viewpurchase,name="viewpurchase"),
    path('updatepurchase/<pk>',views.updatepurchase,name="updatepurchase"),
    path('purchaseinvoice/<pk>',views.purchaseinvoice,name="purchaseinvoice"),
    # Ajax Call for Purchase Start here Estimate
    path('supplierdueamount_estimate/',views.supplierdueamount_estimate,name="supplierdueamount_estimate"),
    path('purchaseprice_estimate/',views.purchaseprice_estimate,name="purchaseprice_estimate"),
    path('estimatepurchasec/',views.estimatepurchasec,name="estimatepurchasec"),
    path('getproducts_estimate/',views.getproducts_estimate,name="getproducts_estimate"),
    path('supplier_product/', views.supplier_products, name="supplier_product"),
    # Ajax Call for Purchase start here GST
    path('supplier_state_gst/',views.supplier_state_gst,name="supplier_state_gst"),
    path('gstpurchasec/',views.gstpurchasec,name="gstpurchasec"),
    path('ownerstate_gst/',views.ownerstate_gst,name="ownerstate_gst"),
    path('purchaseprice_gst/',views.purchaseprice_gst,name="purchaseprice_gst"),
]
