import itertools

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import redirect, render
from num2words import num2words
from django.db.models import F

from customer.models import *
from daybook.models import *
from payments.models import *
from products.models import *
from sales.models import *
from supplier.models import *


# Create your views here.
@login_required(login_url='login')
def list_stock(request):
    try:   
        if request.method == 'POST':
            if request.user.groups.filter(name='Estimate').exists():
                stockdata = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['product_name']))
                stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                stockdata.save()

            if request.user.groups.filter(name='GST').exists():
                stockdata = Stock_gst.objects.get(product = Product_gst.objects.get(product_name=request.POST['product_name']))
                stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                stockdata.save()

        if request.user.groups.filter(name='Estimate').exists():
            stock_data = Stock_estimate.objects.all()
            
        if request.user.groups.filter(name='GST').exists():
            stock_data = Stock_gst.objects.all()

        context = {
            'stock_data' : stock_data
        }
        return render(request, 'statements/stock.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def customer_payment_list(request):
    if request.user.groups.filter(name='Estimate').exists():
        customer_payment = customerpay_estimate.objects.all()
    
    if request.user.groups.filter(name='GST').exists():
        customer_payment = customerpay_gst.objects.all()

    context = {
        'customer_payment':customer_payment
    }
    return render(request, 'statements/customerpaymentlist.html',context)

@login_required(login_url='login')
def supplier_payment_list(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            supplier_payment = supplierpay_estimate.objects.all()
            
        if request.user.groups.filter(name='GST').exists():
            supplier_payment = supplierpay_gst.objects.all()
        
        context = {
            'supplier_payment':supplier_payment
        }
        return render(request,"statements/supplierpaymentlist.html",context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def customer_Credit(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            customer_credit_data = customeraccount_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            customer_credit_data = customeraccount_gst.objects.all()
        
        context = {
            'customer_credit_data':customer_credit_data
        }
        return render(request, 'statements/customercredit.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def supplier_credit(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            supplier_credit_list = supplieraccount_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            supplier_credit_list = supplieraccount_gst.objects.all()

        context = {
            'supplier_credit_list':supplier_credit_list
        }
        return render(request,'statements/suppliercredit.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def totalincome(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            daily_income_data = dailyincome_estimate.objects.all()
            customer_income_data = customerpay_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            daily_income_data = dailyincome_gst.objects.all()
            customer_income_data = customerpay_gst.objects.all()

        context = {
            'daily_income_data':daily_income_data,
            'customer_income_data':customer_income_data
        }
        return render(request,'statements/totalincome.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def totalexpense(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            daily_expense_data = dailyexpense_estimate.objects.all()
            supplier_expense_data = supplierpay_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            daily_expense_data = dailyexpense_gst.objects.all()
            supplier_expense_data = supplierpay_gst.objects.all()
        
        context = {
            'daily_expense_data':daily_expense_data,
            'supplier_expense_data':supplier_expense_data
        }
        return render(request,'statements/totalexpense.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def salereport(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            if request.method == 'POST':
                searchsale = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                context = {
                    'searchsale' : searchsale
                }
                return render(request,'statements/salereport.html',context)

        if request.user.groups.filter(name='GST').exists():
            if request.method == 'POST':
                searchsale = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                context = {
                    'searchsale' : searchsale
                }
                return render(request,'statements/salereport.html',context)

        total_estimate_sale = Estimate_sales.objects.all()
        total_gst_sale = gstsale.objects.all()
        
        context = {
            'total_estimate_sale' : total_estimate_sale,
            'total_gst_sale' : total_gst_sale,
        }
        return render(request,'statements/salereport.html',context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def outofstock(request):
    if request.user.groups.filter(name='Estimate').exists():
        if request.method=='GET':
            stocks_with_min_quantity = Stock_estimate.objects.annotate(min_stock=F('product__minimum_stock')).filter(quantity__lte=F('min_stock'))
            context = {
                'stocks_with_min_quantity': stocks_with_min_quantity
            }
            return render(request, 'statements/outofstock.html', context)

@login_required(login_url='login')
def customerstatement(request):
    if request.user.groups.filter(name='Estimate').exists():
        customer_data = Customer_estimate.objects.all()
        customer_pending_amount = customeraccount_estimate.objects.all()
    
    if request.user.groups.filter(name='GST').exists():
        customer_data = Customer_gst.objects.all()
        customer_pending_amount = customeraccount_estimate.objects.all()

    context = {
        'customer_data' : customer_data
    }
    return render(request,'statements/customerstatement.html',context)

@login_required(login_url='login')
def customer_statement_view(request,pk):
    if request.method == "POST":
        if request.user.groups.filter(name='Estimate').exists():
            sale_data = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).filter(customer = Customer_estimate.objects.get(pk=pk))
            
            if sale_data.count() > 0:
                sale_data_total_filter =  sale_data.aggregate(Sum('Total_amount'))
                sale_data_total = sale_data_total_filter['Total_amount__sum']
                sale_data_round_off_filter = sale_data.aggregate(Sum('Round_off')) 
                sale_data_round_off = sale_data_round_off_filter['Round_off__sum']
            else:
                sale_data_total = 0
                sale_data_round_off = 0


            if sale_data.count() == 0:
                sale_data_money = 0
            else:
                sale_data_money = sale_data_total - sale_data_round_off
                sale_data_money = round(sale_data_money , 2)
                print(sale_data_money)

            payment_data = customerpay_estimate.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).filter(customer_name = Customer_estimate.objects.get(pk=pk))
            payment_data_total_money = 0
            payment_data_round_off_money = 0
            if payment_data.count() > 0:
                payment_data_total_filter = payment_data.aggregate(Sum('paid_amount'))
                payment_data_total = payment_data_total_filter['paid_amount__sum']
                payment_data_round_off_filter = payment_data.aggregate(Sum('round_off'))
                payment_data_round_off = payment_data_round_off_filter['round_off__sum']
                payment_data_total_plus_round_off = float(payment_data_total) + float(payment_data_round_off)
            else:
                payment_data_total = 0
                payment_data_round_off = 0

            if payment_data.count() == 0:
                payment_data_money = 0
            else:
                payment_data_total_money = round(payment_data_total_plus_round_off , 2)
                payment_data_round_off_money = round(payment_data_round_off , 2)

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
        
        if request.user.groups.filter(name='GST').exists():
            sale_data = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])
            payment_data = customerpay_gst.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

            context = {
                'sale_data' : sale_data,
                'payment_data' : payment_data
            }
            return render(request , 'statements/customer_statement_view.html',context)

    return render(request , 'statements/customer_statement_view.html')