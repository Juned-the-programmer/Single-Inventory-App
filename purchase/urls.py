from django.urls import path
from . import views

urlpatterns = [
    path('addpurchase/',views.addpurchase,name="addpurchase"),
    path('viewpurchase/',views.viewpurchase,name="viewpurchase"),
    path('updatepurchase/<pk>',views.updatepurchase,name="updatepurchase"),
    path('purchaseinvoice/<pk>',views.purchaseinvoice,name="purchaseinvoice"),

    # Ajax Call for Purchase Start here Estimate
    path('supplierdueamount_estimate/',views.supplierdueamount_estimate,name="supplierdueamount_estimate"),
    path('purchaseprice_estimate/',views.purchaseprice_estimate,name="purchaseprice"),
    path('supplier_product/', views.supplier_products, name="supplier_product"),
]
