import itertools

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import redirect, render
from num2words import num2words
from django.db.models import F
from django.core.cache import cache

from customer.models import *
from daybook.models import *
from payments.models import *
from products.models import *
from sales.models import *
from supplier.models import *
from Inventory.cache_storage import *

# To generate the different report.

# To list the stock data for every product.
@login_required(login_url='login')
def list_stock(request):
    try:   
        if request.method == 'POST':
            # Check for user Group
            if request.session['Estimate']:
                # Get the stock detail for that product based on the product_name
                stockdata = Stock_estimate.objects.get(product = request.POST['product_name'])
                # Update the quantity
                stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                # Save
                stockdata.save()
            
            # Check for User Group
            if request.session['GST']:
                # Get the stock detail for that product based on the product_name
                stockdata = Stock_gst.objects.get(product = request.POST['product_name'])
                # Update the stock quantity
                stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                # Save
                stockdata.save()

        # Check for the user Group
        if request.session['Estimate']:
            # Get all the stock data for Estimate
            stock_data = Stock_estimate.objects.select_related('product').all()
        
        # Check for User Group
        if request.session['GST']:
            # Get all the stock data for GST
            stock_data = Stock_gst.objects.select_related('product').all()

        context = {
            'stock_data' : stock_data
        }
        return render(request, 'statements/stock.html',context)
    except:
        return redirect('error404')

# To List the customers Payments
@login_required(login_url='login')
def customer_payment_list(request):
    # Check for user Group
    if request.session['Estimate']:
        # Get all the customer Payment for Estimate
        customer_payment = customerpay_estimate.objects.select_related('customer_name').all().order_by("-date")
    
    # Check for User Group
    if request.session['GST']:
        # Get all the Customer Payment for GST
        customer_payment = customerpay_gst.objects.select_related('customer_name').all().order_by("-date")

    context = {
        'customer_payment':customer_payment
    }
    return render(request, 'statements/customerpaymentlist.html',context)

# To List the supplier Payments
@login_required(login_url='login')
def supplier_payment_list(request):
    try:
        # Check for User GRoup
        if request.session['Estimate']:
            # Get all the supplier payments for Estimate
            supplier_payment = supplierpay_estimate.objects.select_related('supplier_name').all().order_by("-date")
            
        # Check for user Group
        if request.session['GST']:
            # Get all the supplier payments for GST
            supplier_payment = supplierpay_gst.objects.select_related('supplier_name').all().order_by("-date")
        
        context = {
            'supplier_payment':supplier_payment
        }
        return render(request,"statements/supplierpaymentlist.html",context)
    except:
        return redirect('error404')

# To list the customer Credit [ What is the pending amount ]
@login_required(login_url='login')
def customer_Credit(request):
    try:
        # Check for user group
        if request.session['Estimate']:
            # Get all the customer credit for Estimate
            customer_credit_data = customeraccount_estimate.objects.select_related('customer_name').all()
        
        # Check for User Group
        if request.session['GST']:
            # Get all the customer creadit for GST
            customer_credit_data = customeraccount_gst.objects.select_related('customer_name').all()
        
        context = {
            'customer_credit_data':customer_credit_data
        }
        return render(request, 'statements/customercredit.html',context)
    except:
        return redirect('error404')

# To list the supplier credit [ What is pending amount ]
@login_required(login_url='login')
def supplier_credit(request):
    try:
        # Check for User Group
        if request.session['Estimate']:
            # Get all the supplier credit for Estimate
            supplier_credit_list = supplieraccount_estimate.objects.select_related('supplier_name').all()
        
        # Check for User Group
        if request.session['GST']:
            # Get all the supplier credit for GST
            supplier_credit_list = supplieraccount_gst.objects.select_related('supplier_name').all()

        context = {
            'supplier_credit_list':supplier_credit_list
        }
        return render(request,'statements/suppliercredit.html',context)
    except:
        return redirect('error404')

# To get the details for total Income data.
@login_required(login_url='login')
def totalincome(request):
    try:
        # Check for User Group
        if request.session['Estimate']:
            # Get the daily Income data
            daily_income_data = dailyincome_estimate.objects.all()
            # Get the customer payment data
            customer_income_data = customerpay_estimate.objects.select_related('customer_name').all().order_by("-date")
        
        # Check for User Group
        if request.session['GST']:
            # Get the daily Income data
            daily_income_data = dailyincome_gst.objects.all()
            # Get the customer payment data
            customer_income_data = customerpay_gst.objects.select_related('customer_name').all().order_by("-date")

        context = {
            'daily_income_data':daily_income_data,
            'customer_income_data':customer_income_data
        }
        return render(request,'statements/totalincome.html',context)
    except:
        return redirect('error404')

# To get the detail for total expense data
@login_required(login_url='login')
def totalexpense(request):
    try:
        # Check for user Group
        if request.session['Estimate']:
            # Get the daily Expense data
            daily_expense_data = dailyexpense_estimate.objects.all()
            # Get the supplier payment data
            supplier_expense_data = supplierpay_estimate.objects.select_related('supplier_name').all().order_by("-date")
        
        # Check for User Group
        if request.session['GST']:
            # Get the daily Expense data
            daily_expense_data = dailyexpense_gst.objects.all()
            # Get the supplier payment data
            supplier_expense_data = supplierpay_gst.objects.select_related('supplier_name').all().order_by("-date")
        
        context = {
            'daily_expense_data':daily_expense_data,
            'supplier_expense_data':supplier_expense_data
        }
        return render(request,'statements/totalexpense.html',context)
    except:
        return redirect('error404')

# To generate the sale report.
''' We will accept the from data and to date and we will get all the sale data between that span of dates '''
@login_required(login_url='login')
def salereport(request):
    try:
        # Check for User Group
        if request.session['Estimate']:
            if request.method == 'POST':
                # Search from the sale data between two dates.
                searchsale = Estimate_sales.objects.filter(date__range = (request.POST['fromdate'] , request.POST['todate'])).select_related('customer')

                context = {
                    'searchsale' : searchsale
                }
                return render(request,'statements/salereport.html',context)

        # Check for user Group
        if request.session['GST']:
            if request.method == 'POST':
                # Serach from the sales data between two dates
                searchsale = gstsale.objects.filter(date__range = (request.POST['fromdate'] , request.POST['todate'])).select_related('customer_name')

                context = {
                    'searchsale' : searchsale
                }
                return render(request,'statements/salereport.html',context)

        return render(request,'statements/salereport.html')
    except:
        return redirect('error404')

# Get the out of stock data 
''' If we remember then while adding a product we are asking for minimum quantity 
if the stock for that product is less than that value then we will display that records here'''
@login_required(login_url='login')
def outofstock(request):
    # Check for User Group
    if request.session['Estimate']:
        if request.method=='GET':
            # Get the stock data which has minimum quantity
            stocks_with_min_quantity = Stock_estimate.objects.annotate(min_stock=F('product__minimum_stock')).filter(quantity__lte=F('min_stock'))
            context = {
                'stocks_with_min_quantity': stocks_with_min_quantity
            }
            return render(request, 'statements/outofstock.html', context)

# Customer Statement for sale report. 
''' This is the first phase of that here we are displaying all the customer data from this customer data we can select any one and generate the report '''
@login_required(login_url='login')
def customerstatement(request):
    # Check for user Group
    if request.session['Estimate']:
        # Get the customer data for Estimate
        customer_data = customer_cache()
    
    # Check for User Group
    if request.session['GST']:
        # Get the customer data for GST
        customer_data = customer_cache_gst()

    context = {
        'customer_data' : customer_data
    }
    return render(request,'statements/customerstatement.html',context)

# To view the satement for that selected customer
''' After selecting customer we have to select the date Range and we will generate the report for that date range. '''
@login_required(login_url='login')
def customer_statement_view(request,pk):
    if request.method == "POST":
        # Check for User Group
        if request.session['Estimate']:
            # Load a cache Customer Data
            customer_data = customer_cache()
            
            customer_data = customer_data.get(id=pk)
            
            # Get the sale data from estimate using filter like dates and customer
            sale_data = customer_data.estimate_sales.filter(date__range=(request.POST['fromdate'], request.POST['todate']))
            
            # Processing data.
            if sale_data.exists():
                sale_data_aggregates = sale_data.aggregate(
                    total_amount_sum=Sum('Total_amount'),
                    round_off_sum=Sum('Round_off')
                )
                sale_data_total = sale_data_aggregates.get('total_amount_sum', 0) or 0
                sale_data_round_off = sale_data_aggregates.get('round_off_sum', 0) or 0
                sale_data_money = sale_data_total - sale_data_round_off
                sale_data_money = round(sale_data_money , 2)
            else:
                sale_data_total = 0
                sale_data_round_off = 0
                sale_data_money = 0

            # Get the payment data for that customer.
            payment_data = customer_data.customerpay_estimate_set.filter(date__range=(request.POST['fromdate'], request.POST['todate']))
            payment_data_total_money = 0
            payment_data_round_off_money = 0

            # Processing data
            if payment_data.exists():
                payment_data_aggregates = payment_data.aggregate(
                    payment_data_total = Sum('paid_amount'),
                    payment_data_round_off = Sum('round_off')
                )
                payment_data_total = payment_data_aggregates.get('payment_data_total' , 0) or 0
                payment_data_round_off = payment_data_aggregates.get('payment_data_round_off' ,  0) or 0
                payment_data_total_plus_round_off = float(payment_data_total) + float(payment_data_round_off)
                payment_data_total_money = round(payment_data_total_plus_round_off , 2)
                payment_data_round_off_money = round(payment_data_round_off , 2)
            else:
                payment_data_total = 0
                payment_data_round_off = 0
                payment_data_total_money = 0
                payment_data_round_off_money = 0

            total_data = itertools.zip_longest(payment_data,sale_data)

            context = {
                'sale_data_total' : sale_data_total,
                'sale_data_money' : sale_data_money,
                'total_data' : total_data,
                'payment_data_total' : payment_data_total,
                'payment_data_total_money' : payment_data_total_money,
                'payment_data_round_off_money' : payment_data_round_off_money,
                'sale_date_round_off' : sale_data_round_off
            }
            return render(request , 'statements/customer_statement_view.html',context)
        
        if request.session['GST']:
            # Load a cache Customer Data
            customer_data = customer_cache_gst()
            
            customer_data = customer_data.get(id=pk)
            
            # Get the sale data from estimate using filter like dates and customer
            sale_data = customer_data.gst_sales.filter(date__range=(request.POST['fromdate'], request.POST['todate']))
            
            # Processing data.
            if sale_data.exists():
                sale_data_aggregates = sale_data.aggregate(
                    total_amount_sum=Sum('Grand_total'),
                    round_off_sum=Sum('Round_off')
                )
                sale_data_total = sale_data_aggregates.get('total_amount_sum', 0) or 0
                sale_data_round_off = sale_data_aggregates.get('round_off_sum', 0) or 0
                sale_data_money = sale_data_total - sale_data_round_off
                sale_data_money = round(sale_data_money , 2)
            else:
                sale_data_total = 0
                sale_data_round_off = 0
                sale_data_money = 0

            # Get the payment data for that customer.
            payment_data = customer_data.customerpay_gst_set.filter(date__range=(request.POST['fromdate'], request.POST['todate']))
            payment_data_total_money = 0
            payment_data_round_off_money = 0

            # Processing data
            if payment_data.exists():
                payment_data_aggregates = payment_data.aggregate(
                    payment_data_total = Sum('paid_amount'),
                    payment_data_round_off = Sum('round_off')
                )
                payment_data_total = payment_data_aggregates.get('payment_data_total' , 0) or 0
                payment_data_round_off = payment_data_aggregates.get('payment_data_round_off' ,  0) or 0
                payment_data_total_plus_round_off = float(payment_data_total) + float(payment_data_round_off)
                payment_data_total_money = round(payment_data_total_plus_round_off , 2)
                payment_data_round_off_money = round(payment_data_round_off , 2)
            else:
                payment_data_total = 0
                payment_data_round_off = 0
                payment_data_total_money = 0
                payment_data_round_off_money = 0

            total_data = itertools.zip_longest(payment_data,sale_data)

            context = {
                'sale_data_total' : sale_data_total,
                'sale_data_money' : sale_data_money,
                'total_data' : total_data,
                'payment_data_total' : payment_data_total,
                'payment_data_total_money' : payment_data_total_money,
                'payment_data_round_off_money' : payment_data_round_off_money,
                'sale_date_round_off' : sale_data_round_off
            }
            return render(request , 'statements/customer_statement_view.html',context)

    return render(request , 'statements/customer_statement_view.html')