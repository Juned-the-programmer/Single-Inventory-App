from django.urls import path
from . import views

urlpatterns = [
    # Daily Income/Expense
    path('dailyincome/',views.dailyincome,name="dailyincome"),
    path('dailyexpense/',views.dailyexpense,name="dailyexpense"),

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
    path('outofstock/',views.outofstock,name="outofstock"),
    path('customerstatement/',views.customerstatement,name="customerstatement"),
    path('customer_statement_view/<pk>',views.customer_statement_view,name="customer_statement_view")
]
