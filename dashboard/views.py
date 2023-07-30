from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from .models import *
from pages.models import *
from django.contrib import messages
from django.http import  HttpResponse , JsonResponse
from datetime import date
from num2words import num2words
import itertools
from django.db.models import Sum,Min,Max,Avg
# Create your views here

# Daily Income / Expense
@login_required(login_url='login')
def dailyincome(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:

                    DailyIncome = dailyincome_estimate(
                        name=request.POST['name'],
                        amount=request.POST['amount']
                    )
                    DailyIncome.save()
                    messages.success(request,"Daily Income Added Successfully !")
                else:
                    DailyIncome = dailyincome_gst(
                        name = request.POST['name'],
                        amount=request.POST['amount']
                    )
                    DailyIncome.save()
                    messages.success(request,"Daily DailyIncome Successfully ! ")
            
            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            d2 = date_.strftime("%Y-%m-%d")

            if Estimate_group in user.groups.all():
                Dailyincome_data = dailyincome_estimate.objects.filter(date=d2)

            if GST_group in user.groups.all():
                Dailyincome_data = dailyincome_gst.objects.filter(date=d2)

            context = {
                'd1':d1,
                'Dailyincome_data' : Dailyincome_data
            }
            return render(request, 'dashboard/dailyincome.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def dailyexpense(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'GST' in request.POST:
                    DailyExpense = dailyexpense_gst(
                        category=request.POST['category'],
                        amount=request.POST['amount'],
                        name=request.POST['name']
                    )
                    DailyExpense.save()

                elif 'addcategory_gst' in request.POST:
                    Category = category_gst(
                        category_name=request.POST['cat'],
                    )
                    Category.save()

                elif 'Estimate' in request.POST:
                    DailyExpense = dailyexpense_estimate(
                        category=request.POST['category'],
                        amount=request.POST['amount'],
                        name=request.POST['name']
                    )
                    DailyExpense.save()

                else:
                    Category = category_estimate(
                        category_name=request.POST['cat'],
                    )
                    Category.save()
            
            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            d2 = date_.strftime("%Y-%m-%d")

            if Estimate_group in user.groups.all():
                DailyExpense_data = dailyexpense_estimate.objects.filter(date=d2)
                category_data = category_estimate.objects.all()

            if GST_group in user.groups.all():
                DailyExpense_data = dailyexpense_gst.objects.filter(date=d2)
                category_data = category_gst.objects.all()

            context = {
                'd1':d1,
                'DailyExpense_data' : DailyExpense_data,
                'category_data' : category_data
            }
            return render(request , 'dashboard/dailyexpense.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def supplierpayment(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:
                
                if len(request.POST['round_off']) >= 1:
                    round_off = request.POST['round_off']
                else:
                    round_off = 0

                SupplierPay = supplierpay_estimate(
                    supplier_name = Supplier_estimate.objects.get(id=request.POST['supplier-name']),
                    pending_amount = float(request.POST['pending_amount']),
                    paid_amount = float(request.POST['paid_amount']),
                    round_off = round_off
                )
            
                supplieraccountdata = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(id=request.POST['supplier-name']).id)

                supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
                supplieraccountdata.amount = supplieraccountdata.amount - float(round_off)

                supplieraccountdata.save()
                SupplierPay.save()
                messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

            else:
                
                if len(request.POST['round_off']) >= 1:
                    round_off = request.POST['round_off']
                else:
                    round_off = 0

                SupplierPay = supplierpay_gst(
                    supplier_name = supplieraccount_gst.objects.get(id=request.POST['supplier-name']).supplier_name,
                    pending_amount = float(request.POST['pending_amount']),
                    paid_amount = float(request.POST['paid_amount']),
                    round_off = round_off
                )
            
                supplieraccountdata = supplieraccount_gst.objects.get(id=request.POST['supplier-name'])

                supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
                supplieraccountdata.amount = supplieraccountdata.amount - float(round_off)

                supplieraccountdata.save()
                SupplierPay.save()
                messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

        if Estimate_group in user.groups.all():
            supplier_data = Supplier_estimate.objects.all()

        if GST_group in user.groups.all():
            supplier_data = Supplier_gst.objects.all()

        date_ = date.today()
        d1 = date_.strftime("%d/%m/%Y")
        context = {
            'd1':d1,
            'supplier_data':supplier_data
        }
        return render(request, 'dashboard/supplierpayment.html',context)
    else:
        return redirect('login')

@login_required(login_url='login')
def customerpayment(request):
    Estimate_group = Group.objects.get(name="Estimate")
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:

                    if len(request.POST['round_off']) >= 1:
                        round_off = request.POST['round_off']
                    else:
                        round_off = 0

                    CustomerPay = customerpay_estimate (
                        customer_name = customeraccount_estimate.objects.get(id=request.POST['customer']).customer_name,
                        pending_amount = request.POST['pending_amount'],
                        paid_amount = request.POST['paid_amount'],
                        round_off = round_off,
                        Description = request.POST['Description']
                    )
                    CustomerPay.save()

                    customerdata = customeraccount_estimate.objects.get(id=request.POST['customer'])

                    customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
                    customerdata.amount = customerdata.amount - float(round_off)

                    customerdata.save()
                    messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")

                else:

                    if len(request.POST['round_off']) >= 1:
                        round_off = request.POST['round_off']
                    else:
                        round_off = 0

                    CustomerPay = customerpay_gst (
                        customer_name = customeraccount_gst.objects.get(id=request.POST['customer']).customer_name,
                        pending_amount = request.POST['pending_amount'],
                        paid_amount = request.POST['paid_amount'],
                        round_off = round_off,
                        Description = request.POST['Description']
                    )
                    CustomerPay.save()

                    customerdata = customeraccount_gst.objects.get(id=request.POST['customer'])

                    customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
                    customerdata.amount = customerdata.amount - float(round_off)

                    customerdata.save()
                    messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")
            

            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            if Estimate_group in user.groups.all():
                customer_data = customeraccount_estimate.objects.all()
            
            if GST_group in user.groups.all():
                customer_data = customeraccount_gst.objects.all()

            context = {
                'd1':d1,
                'customer_data':customer_data
            }
            return render(request, 'dashboard/customerpayment.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def supplier_dueamount_estimate(request):
    sid = request.GET['sid']
    supplierdata = supplieraccount_estimate.objects.get(id = supplieraccount_estimate.objects.get(supplier_name = sid).id)
    pendingamount = supplierdata.amount

    return HttpResponse(pendingamount)

@login_required(login_url='login')
def customer_dueamount_estimate(request):
    cid = request.GET['cid']
    customerdata = customeraccount_estimate.objects.get(id = customeraccount_estimate.objects.get(id=cid).id)
    pendingamount = customerdata.amount

    return HttpResponse(pendingamount)

@login_required(login_url='login')
def customer_dueamount_gst(request):
    cid = request.GET['cid']
    customerdata = customeraccount_gst.objects.get(id = customeraccount_gst.objects.get(id=cid).id)
    pendingamount = customerdata.amount

    return HttpResponse(pendingamount)

@login_required(login_url='login')
def supplier_dueamount_gst(request):
    sid = request.GET['sid']
    supplierdata = supplieraccount_gst.objects.get(id = supplieraccount_gst.objects.get(id=sid).id)
    pendingamount = supplierdata.amount

    return HttpResponse(pendingamount)


# Statements
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
            return render(request, 'dashboard/stock.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def customer_payment_list(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                customer_payment = customerpay_estimate.objects.all()
            else:
                customer_payment = customerpay_gst.objects.all()

            context = {
                'customer_payment':customer_payment
            }
            return render(request, 'dashboard/customerpaymentlist.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

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
            return render(request,"dashboard/supplierpaymentlist.html",context)
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
            return render(request, 'dashboard/customercredit.html',context)
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
            return render(request,'dashboard/suppliercredit.html',context)
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
            return render(request,'dashboard/totalincome.html',context)
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
            return render(request,'dashboard/totalexpense.html',context)
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
                        return render(request,'dashboard/salereport.html',context)

            if GST_group in user.groups.all():
                if request.method == 'POST':
                    if 'GST' in request.POST:
                        searchsale = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                        context = {
                            'searchsale' : searchsale
                        }
                        return render(request,'dashboard/salereport.html',context)

            total_estimate_sale = Estimate_sales.objects.all()
            total_gst_sale = gstsale.objects.all()
            
            context = {
                'total_estimate_sale' : total_estimate_sale,
                'total_gst_sale' : total_gst_sale,
            }
            return render(request,'dashboard/salereport.html',context)
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
    return render(request,'dashboard/outofstock.html')

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
    return render(request,'dashboard/customerstatement.html',context)

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
                return render(request , 'dashboard/customer_statement_view.html',context)
            else:
                sale_data = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])
                payment_data = customerpay_gst.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                context = {
                    'sale_data' : sale_data,
                    'payment_data' : payment_data
                }
                return render(request , 'dashboard/customer_statement_view.html',context)
    else:
        return redirect('login')

    return render(request , 'dashboard/customer_statement_view.html')