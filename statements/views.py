import itertools

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import redirect, render
from num2words import num2words

from customer.models import *
from daybook.models import *
from payments.models import *
from products.models import *
from sales.models import *
from supplier.models import *


# Create your views here.
@login_required(login_url='login')
def list_stock(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:    
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    stockdata = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['product_name']))
                    stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                    stockdata.save()

                if 'GST' in request.POST:
                    stockdata = Stock_gst.objects.get(product = Product_gst.objects.get(product_name=request.POST['product_name']))
                    stockdata.quantity = stockdata.quantity + int(request.POST['qty'])
                    stockdata.save()

            if Estimate_group in user.groups.all():
                stock_data = Stock_estimate.objects.all()
            else:
                stock_data = Stock_gst.objects.all()

            context = {
                'stock_data' : stock_data
            }
            return render(request, 'statements/stock.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def customer_payment_list(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if Estimate_group in user.groups.all():
            customer_payment = customerpay_estimate.objects.all()
        else:
            customer_payment = customerpay_gst.objects.all()

        context = {
            'customer_payment':customer_payment
        }
        return render(request, 'statements/customerpaymentlist.html',context)
    else:
        return redirect('login')

@login_required(login_url='login')
def supplier_payment_list(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                supplier_payment = supplierpay_estimate.objects.all()
            else:
                supplier_payment = supplierpay_gst.objects.all()
            
            context = {
                'supplier_payment':supplier_payment
            }
            return render(request,"statements/supplierpaymentlist.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def customer_Credit(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                customer_credit_data = customeraccount_estimate.objects.all()
            else:
                customer_credit_data = customeraccount_gst.objects.all()
            
            context = {
                'customer_credit_data':customer_credit_data
            }
            return render(request, 'statements/customercredit.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def supplier_credit(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                supplier_credit_list = supplieraccount_estimate.objects.all()
            else:
                supplier_credit_list = supplieraccount_gst.objects.all()

            context = {
                'supplier_credit_list':supplier_credit_list
            }
            return render(request,'statements/suppliercredit.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def totalincome(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                daily_income_data = dailyincome_estimate.objects.all()
                customer_income_data = customerpay_estimate.objects.all()
            else:
                daily_income_data = dailyincome_gst.objects.all()
                customer_income_data = customerpay_gst.objects.all()

            context = {
                'daily_income_data':daily_income_data,
                'customer_income_data':customer_income_data
            }
            return render(request,'statements/totalincome.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def totalexpense(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                daily_expense_data = dailyexpense_estimate.objects.all()
                supplier_expense_data = supplierpay_estimate.objects.all()
            else:
                daily_expense_data = dailyexpense_gst.objects.all()
                supplier_expense_data = supplierpay_gst.objects.all()
            
            context = {
                'daily_expense_data':daily_expense_data,
                'supplier_expense_data':supplier_expense_data
            }
            return render(request,'statements/totalexpense.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def salereport(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                if request.method == 'POST':
                    if 'Estimate' in request.POST:
                        searchsale = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                        context = {
                            'searchsale' : searchsale
                        }
                        return render(request,'statements/salereport.html',context)

            if GST_group in user.groups.all():
                if request.method == 'POST':
                    if 'GST' in request.POST:
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
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def getsupplier(request):
    sid = request.GET['sid']
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if Estimate_group in user.groups.all():
        supplier = supplieraccount_estimate.objects.get(id=1)
        amount = supplier.amount
        print(amount)
    else:
        supplier = supplieraccount_estimate.objects.get(id=1)
        amount = supplier.amount
        print(amount)
    
    return HttpResponse(amount)

def outofstock(request):
    return render(request,'statements/outofstock.html')

def customerstatement(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    
    if Estimate_group in user.groups.all():
        customer_data = Customer_estimate.objects.all()
        customer_pending_amount = customeraccount_estimate.objects.all()
    else:
        customer_data = Customer_gst.objects.all()
        customer_pending_amount = customeraccount_estimate.objects.all()

    context = {
        'customer_data' : customer_data
    }
    return render(request,'statements/customerstatement.html',context)

def customer_statement_view(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)

    if user.is_authenticated:
        if request.method == "POST":
            if "Estimate" in request.POST:
                sale_data = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).filter(customer = Customer_estimate.objects.get(pk=pk))
                
                sale_data_total_filter =  Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).aggregate(Sum('Total_amount'))
                sale_data_total = sale_data_total_filter['Total_amount__sum']
                sale_data_round_off_filter = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).aggregate(Sum('Round_off')) 
                sale_data_round_off = sale_data_round_off_filter['Round_off__sum']

                if sale_data.count() == 0:
                    sale_data_money = 0
                else:
                    sale_data_money = sale_data_total - sale_data_round_off
                    sale_data_money = round(sale_data_money , 2)
                    print(sale_data_money)

                payment_data = customerpay_estimate.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])
                payment_data_total_money = 0
                payment_data_round_off_money = 0
                if customerpay_estimate.objects.all().count() >= 0 and payment_data.count() >= 0:
                    payment_data_total_filter = customerpay_estimate.objects.filter(date__gte=request.POST['fromdate'] , date__lte = request.POST['todate']).aggregate(Sum('paid_amount'))
                    payment_data_total = payment_data_total_filter['paid_amount__sum']
                    payment_data_round_off_filter = customerpay_estimate.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate']).aggregate(Sum('round_off'))
                    payment_data_round_off = payment_data_round_off_filter['round_off__sum']
                else:
                    payment_data_total = 0
                    payment_data_round_off = 0

                if payment_data.count() == 0:
                    payment_data_money = 0
                else:
                    payment_data_total_money = round(payment_data_total , 2)
                    payment_data_round_off_money = round(payment_data_round_off , 2)

                total_data = itertools.zip_longest(payment_data,sale_data)
                print(total_data)

                context = {
                    'sale_data_money' : sale_data_money,
                    'total_data' : total_data,
                    'payment_data_total_money' : payment_data_total_money,
                    'payment_data_round_off_money' : payment_data_round_off_money
                }
                return render(request , 'statements/customer_statement_view.html',context)
            else:
                sale_data = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])
                payment_data = customerpay_gst.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                context = {
                    'sale_data' : sale_data,
                    'payment_data' : payment_data
                }
                return render(request , 'statements/customer_statement_view.html',context)
    else:
        return redirect('login')

    return render(request , 'statements/customer_statement_view.html')