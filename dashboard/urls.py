from django.urls import path
from . import views

urlpatterns = [
    path('addcustomer/',views.addcustomer,name="addcustomer"),
    path('viewcustomer/',views.viewcustomer,name="viewcustomer"),
    path('updatecustomer/<pk>',views.updatecustomer,name="updatecustomer"),

    path('addsupplier/',views.addsupplier,name="addsupplier"),
    path('viewsupplier/',views.viewsupplier,name="viewsupplier"),
    path('updatesupplier/<pk>',views.updatesupplier,name="updatesupplier"),

    path('addproduct/',views.addproduct,name="addproduct"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('updateproduct/<pk>',views.updateproduct,name="updateproduct"),

    path('addpurchase/',views.addpurchase,name="addpurchase"),
    path('viewpurchase/',views.viewpurchase,name="viewpurchase"),
    path('updatepurchase/<pk>',views.updatepurchase,name="updatepurchase"),
    path('purchaseinvoice/<pk>',views.purchaseinvoice,name="purchaseinvoice"),
    # Ajax Call for Purchase Start here Estimate
    path('supplierdueamount_estimate/',views.supplierdueamount_estimate,name="supplierdueamount_estimate"),
    path('purchaseprice_estimate/',views.purchaseprice_estimate,name="purchaseprice_estimate"),
    path('estimatepurchasec/',views.estimatepurchasec,name="estimatepurchasec"),
    path('getproducts_estimate/',views.getproducts_estimate,name="getproducts_estimate"),
    # Ajax Call for Purchase start here GST
    path('supplier_state_gst/',views.supplier_state_gst,name="supplier_state_gst"),
    path('gstpurchasec/',views.gstpurchasec,name="gstpurchasec"),
    path('ownerstate_gst/',views.ownerstate_gst,name="ownerstate_gst"),
    path('purchaseprice_gst/',views.purchaseprice_gst,name="purchaseprice_gst"),

    path('addsale/',views.addsale,name="addsale"),
    path('viewsale/',views.viewsale,name="viewsale"),
    path('updatesale/<pk>',views.updatesale,name="updatesale"),
    path('saleinvoice/<pk>',views.saleinvoice,name="saleinvoice"),
    #Ajax Call for Estimate Sale Start here
    path('estimatesalec/',views.estimatesalec,name="estimatesalec"),
    path('sellingprice_estimate/',views.sellingprice_estimate,name="sellingprice_estimate"),
    path('previous_discount_estimate/',views.previous_discount_estimate,name="previous_discount_estimate"),
    path('customerdue_estimate/',views.customerdue_estimate,name="customerdue_estimate"),
    path('product_data_estimate/',views.product_data_estimate,name="product_data_estimate"),
    path('stock_data_estimate/',views.stock_data_estimate,name="stock_data_estimate"),
    # Ajax Call for GST Sale Start here
    path('gstsalec/',views.gstsalec,name="gstsalec"),
    path('product_data_gst/',views.product_data_gst,name="product_data_gst"),
    path('getproducts_gst_sale/',views.getproducts_gst_sale,name="getproducts_gst_sale"),
    path('customer_state_gst/',views.customer_state_gst,name="customer_state_gst"),
    path('check_stock_gst/',views.check_stock_gst,name="check_stock_gst"),
    path('sellingprice_gst/',views.sellingprice_gst,name="sellingprice_gst"),
    path('ownerstate_gst_sale/',views.ownerstate_gst_sale,name="ownerstate_gst_sale"),

    # Daily Income/Expense
    path('dailyincome/',views.dailyincome,name="dailyincome"),
    path('dailyexpense/',views.dailyexpense,name="dailyexpense"),

    # Customer / Supplier Payment
    path('supplierpayment/',views.supplierpayment,name="supplierpayment"),
    path('customerpayment/',views.customerpayment,name="customerpayment"),
    path('supplier_dueamount_estimate/',views.supplier_dueamount_estimate,name="supplier_dueamount_estimate"),
    path('customer_dueamount_estimate/',views.customer_dueamount_estimate,name="customer_dueamount_estimate"),
    path('customer_dueamount_gst/',views.customer_dueamount_gst,name="customer_dueamount_gst"),
    path('supplier_dueamount_gst/',views.supplier_dueamount_gst,name="supplier_dueamount_gst"),

    #Statements 
    path('list_stock/',views.list_stock,name="list_stock"),
    path('customer_payment_list/',views.customer_payment_list,name="customer_payment_list"),
    path('supplier_payment_list/',views.supplier_payment_list,name="supplier_payment_list"),
    path('customer_Credit/',views.customer_Credit,name="customer_Credit"),
    path('supplier_credit/',views.supplier_credit,name="supplier_credit"),
    path('totalincome/',views.totalincome,name="totalincome"),
    path('totalexpense/',views.totalexpense,name="totalexpense"),
    path('salereport/',views.salereport,name="salereport"),
    path('getsupplier/',views.getsupplier,name="getsupplier"),
]
