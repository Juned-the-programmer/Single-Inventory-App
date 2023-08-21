from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from dashboard.models import *
from products.models import *

from .models import *


# Create your views here.
def estimatesalec(request):
    global esc
    esc=int(request.GET['c'])
    return HttpResponse(esc)

def gstsalec(request):
    global gst
    gst=int(request.GET['c'])
    return HttpResponse(gst)

@login_required(login_url='login')
def addsale(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
            if len(request.POST['cod']):
                cash_on_hand = request.POST['cod']
            else:
                cash_on_hand = 0
            
            if len(request.POST['roff']):
                Round_off = request.POST['roff']
            else:
                Round_off = 0

            Grand_total = request.POST['gtot']
        
            Estimatesale = Estimate_sales(
                Bill_no=request.POST['bill_no'],
                customer = Customer_estimate.objects.get(id=request.POST['customer']),
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )
            customerAccount = customeraccount_estimate.objects.get(customer_name = request.POST['customer'])
            customerAccount.amount = float(Grand_total)
            
            if cash_on_hand == 0:
                print("Customer Payment")
            else:
                CustomerPay = customerpay_estimate (
                    customer_name = request.POST['customer'],
                    pending_amount = Grand_total,
                    paid_amount = cash_on_hand,
                    round_off = 0
                )
                CustomerPay.save()
                customerAccount.amount  = float(customerAccount.amount) - float(cash_on_hand)

            for i in range(0,esc):
                if len(request.POST['dis'+str(i)]) >= 1:
                    dis = request.POST['dis'+str(i)]
                else:
                    dis = 0
                estimate = estimatesales_Product (
                    Bill_no = request.POST['bill_no'],
                    product_name = request.POST['prod'+str(i)],
                    unit = request.POST['unit'+str(i)],
                    rate = request.POST['rate'+str(i)],
                    qty = request.POST['qty'+str(i)],
                    dis = dis,
                    netrate = request.POST['nr'+str(i)],
                    total = request.POST['tot'+str(i)]
                )

                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                b = int(request.POST['qty'+str(i)])
                stock.quantity = a - b
                stock.save()

                estimate.save()

            customerAccount.save()
            Estimatesale.save()

        if request.user.groups.filter(name='GST').exists():
            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
                print(Round_off)
            else:
                Round_off = 0
                print(Round_off )

            if len(request.POST['cgst']) >= 1:
                CGST = request.POST['cgst']
            else:
                CGST = 0

            if len(request.POST['igst']) >= 1:
                IGST = request.POST['igst']
            else:
                IGST = 0

            if len(request.POST['sgst']) >= 1:
                SGST = request.POST['sgst']
            else:
                SGST = 0

            GSTSALE = gstsale (
                Bill_no=request.POST['bill_no'],
                customer_name = Customer_gst.objects.get(id = Customer_gst.objects.get(fullname=request.POST['customer']).id),
                total_amount=request.POST['total'],
                CGST=CGST,
                SGST=SGST,
                IGST=IGST,
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )
            

            GSTCUSTOMER = customeraccount_gst.objects.get(customer_name = Customer_gst.objects.get(fullname=request.POST['customer']))
            GSTCUSTOMER.amount = float(GSTCUSTOMER.amount) + float(request.POST['gtot'])
            

            for i in range(0,gst):
                Gstsale = gstsales_Product (
                    Bill_no = request.POST['bill_no'],
                    hsncode = request.POST['hsn'+str(i)],
                    product_name = request.POST['prod'+str(i)],
                    unit = request.POST['unit'+str(i)],
                    rate = request.POST['rate'+str(i)],
                    qty = request.POST['qty'+str(i)],
                    gstp = request.POST['gstp'+str(i)],
                    gstamt = request.POST['gstamt'+str(i)],
                    total = request.POST['tot'+str(i)]
                )

                stock = Stock_gst.objects.get(product = Product_gst.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                b = int(request.POST['qty'+str(i)])
                stock.quantity = a - b
                stock.save()

                Gstsale.save()
            
            GSTSALE.save()
            GSTCUSTOMER.save()

    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")

    if request.user.groups.filter(name='Estimate').exists():
        Product_data = Product_estimate.objects.all()
        Customer_data = Customer_estimate.objects.all()

        if Estimate_sales.objects.all().exists():
            new_billno = Estimate_sales.objects.all().count()
            new_billno = new_billno + 1
        else:
            new_billno = 1
    
    if request.user.groups.filter(name='GST').exists():
        Product_data = Product_gst.objects.all()
        Customer_data = Customer_gst.objects.all()
        
        if gstsale.objects.all().exists():
            new_billno = gstsale.objects.last().Bill_no
            new_billno = new_billno + 1
        else:
            new_billno = 1

    context = {
        'Product_data' : Product_data,
        'Customer_data' : Customer_data,
        'new_billno' : new_billno,
        'd1' : d1,
    }
    return render(request,"sales/sale.html",context)

@login_required(login_url='login')
def viewsale(request):
    if request.user.groups.filter(name='Estimate').exists():
        Sale_data = Estimate_sales.objects.all()

    if request.user.groups.filter(name='GST').exists():
        Sale_data = gstsale.objects.all()

    context = {
        'Sale_data' : Sale_data
    }
    return render(request,"sales/viewsale.html",context)

@login_required(login_url='login')
def updatesale(request , pk):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
            else:
                Round_off = 0

            Grand_total = request.POST['gtot']
            old_grant_total =  request.POST['cod']

            saleproduct_count = estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
            bill_product = estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no'])
            
            for j in range(0,saleproduct_count):
                print(bill_product[j].product_name)
                add_stock = Stock_estimate.objects.get(product=Product_estimate.objects.get(product_name=bill_product[j].product_name))
                add_stock.quantity = add_stock.quantity + bill_product[j].qty
                add_stock.save()

            Estimate_sales.objects.get(Bill_no=request.POST['bill_no']).delete()
            estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

            Estimatesale = Estimate_sales(
                Bill_no=request.POST['bill_no'],
                customer = Customer_estimate.objects.get(id = Customer_estimate.objects.get(fullname=request.POST['customer']).id),
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=request.POST['roff'],
                Grand_total=request.POST['gtot']
            )
            

            old_amount = float(Grand_total) - float(old_grant_total) 

            customerAccount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']))
            customerAccount.amount = float(customerAccount.amount) + float(old_amount) 
            

            for i in range(0,esc):
                if len(request.POST['dis'+str(i)]) >= 1:
                    dis = request.POST['dis'+str(i)]
                else:
                    dis = 0
                    
                estimate = estimatesales_Product (
                    Bill_no = request.POST['bill_no'],
                    product_name = request.POST['prod'+str(i)],
                    unit = request.POST['unit'+str(i)],
                    rate = request.POST['rate'+str(i)],
                    qty = request.POST['qty'+str(i)],
                    dis = dis,
                    netrate = request.POST['nr'+str(i)],
                    total = request.POST['tot'+str(i)]
                )

                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                b = int(request.POST['qty'+str(i)])
                stock.quantity = a - b
                stock.save()
                estimate.save()

            Estimatesale.save()
            customerAccount.save()
            return redirect('viewsale')
            messages.success(request, "Sale Updated Successfully ! ")

        if request.user.groups.filter(name='GST').exists():

            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
                print(Round_off)
            else:
                Round_off = 0
                print(Round_off )

            if len(request.POST['cgst']) >= 1:
                CGST = request.POST['cgst']
            else:
                CGST = 0

            if len(request.POST['igst']) >= 1:
                IGST = request.POST['igst']
            else:
                IGST = 0

            if len(request.POST['sgst']) >= 1:
                SGST = request.POST['sgst']
            else:
                SGST = 0
            
            old_grant_total = request.POST['grant_total_gst']

            saleproduct_count = gstsales_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
            bill_product = gstsales_Product.objects.filter(Bill_no=request.POST['bill_no'])
            
            for j in range(0,saleproduct_count):
                print(bill_product[j].product_name)
                add_stock = Stock_gst.objects.get(product=Product_gst.objects.get(product_name=bill_product[j].product_name))
                add_stock.quantity = add_stock.quantity + bill_product[j].qty
                add_stock.save()

            gstsale.objects.get(Bill_no=request.POST['bill_no']).delete()
            gstsales_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

            GSTSALE = gstsale (
                Bill_no=request.POST['bill_no'],
                customer_name = Customer_gst.objects.get(id = Customer_gst.objects.get(fullname=request.POST['customer']).id),
                total_amount=request.POST['total'],
                CGST=CGST,
                SGST=SGST,
                IGST=IGST,
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )

            old_amount = float(request.POST['gtot']) - float(old_grant_total)
            
            GSTCUSTOMER = customeraccount_gst.objects.get(customer_name = Customer_gst.objects.get(fullname=request.POST['customer']))
            GSTCUSTOMER.amount = float(GSTCUSTOMER.amount) + float(old_amount)
            

            for i in range(0,gst):
                Gstsale = gstsales_Product (
                    Bill_no = request.POST['bill_no'],
                    hsncode = request.POST['hsn'+str(i)],
                    product_name = request.POST['prod'+str(i)],
                    unit = request.POST['unit'+str(i)],
                    rate = request.POST['rate'+str(i)],
                    qty = request.POST['qty'+str(i)],
                    gstp = request.POST['gstp'+str(i)],
                    gstamt = request.POST['gstamt'+str(i)],
                    total = request.POST['tot'+str(i)]
                )

                stock = Stock_gst.objects.get(product = Product_gst.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                b = int(request.POST['qty'+str(i)])
                stock.quantity = a - b
                stock.save()

                Gstsale.save()
            
            GSTSALE.save()
            GSTCUSTOMER.save()

            return redirect('viewsale')


    if request.user.groups.filter(name='Estimate').exists():
        sale_Bill_no = Estimate_sales.objects.get(pk=pk).Bill_no
        sale_data = Estimate_sales.objects.get(Bill_no=sale_Bill_no)
        sale_product = estimatesales_Product.objects.filter(Bill_no=sale_Bill_no)
        customer_data = Customer_estimate.objects.all()
        product_data = Product_estimate.objects.all()


    if request.user.groups.filter(name='GST').exists():
        sale_Bill_no = gstsale.objects.get(pk=pk).Bill_no
        sale_data = gstsale.objects.get(Bill_no=sale_Bill_no)
        sale_product = gstsales_Product.objects.filter(Bill_no=sale_Bill_no)
        customer_data = Customer_gst.objects.all()
        product_data = Product_gst.objects.all()

    context = {
        'sale_Bill_no' : sale_Bill_no,
        'sale_data' : sale_data,
        'sale_product' : sale_product,
        'customer_data' : customer_data,
        'product_data' : product_data
    }
    return render(request,"sales/updatesale.html",context)

@login_required(login_url='login')
def saleinvoice(request,pk):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            sale_data = Estimate_sales.objects.get(pk=pk)
            product_data = estimatesales_Product.objects.filter(Bill_no = sale_data.Bill_no)
            word = 1

        if request.user.groups.filter(name='GST').exists():
            sale_data = gstsale.objects.get(pk=pk)
            product_data = gstsales_Product.objects.filter(Bill_no = sale_data.Bill_no)
            word =num2words(gst.Grand_total)

        raw_text = u"\u20B9"        
        print(raw_text)

        context = {
            'sale_data' : sale_data,
            'product_data':product_data,
            'word' : word,
            'raw_text' : raw_text,
        }
        return render(request,"sales/saleinvoice.html",context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def sellingprice_estimate(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    rate_ = 0
    last_price = 0
    last_rate = 0
    pk_id = 0
    
    if Estimate_sales.objects.filter(customer = cname).count() >= 1:
        customer_id = Estimate_sales.objects.filter(customer = cname).last()
        pk_id = customer_id.Bill_no

    if estimatesales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).count() >= 1:
        product_rate = estimatesales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).last()
        rate_ = product_rate.rate
        print(rate_)
    else:
        last_price = Product_estimate.objects.get(product_name=pname).selling_price


    if len(str(rate_)) > 1:
        last_rate = rate_
        print(last_rate)
    else:
        last_rate = last_price
        print(last_rate)
        
    return HttpResponse(last_rate)

@login_required(login_url='login')
def previous_discount_estimate(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    rate_ = 0
    last_price = 0
    last_discount = 0
    pk_id = 0
    
    if Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(id=cname)).count() >= 1:
        customer_id = Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(id=cname)).last()
        pk_id = customer_id.Bill_no

    if estimatesales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).count() >= 1:
        product_rate = estimatesales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).last()
        rate_ = product_rate.dis
        print(rate_)
    else:
        last_price = 0.0


    if len(str(rate_)) > 1:
        last_discount = rate_
        print(last_discount)
    else:
        last_discount = last_price
        print(last_discount)

    return HttpResponse(last_discount)

@login_required(login_url='login')
def customerdue_estimate(request):
    cname = request.GET['cname']
    camount = customeraccount_estimate.objects.get(id = cname)
    due_amount = camount.amount

    return HttpResponse(due_amount)

def product_data_estimate(request):
    productdata = Product_estimate.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def stock_data_estimate(request):
    stock_data = Stock_estimate.objects.all()
    return JsonResponse({"stock_data":list(stock_data.values())})

def stock_data_gst(request):
    stock_data = Stock_gst.objects.objects.all()
    return JsonResponse({"stock_data":list(stock_data.values())})

# GST sale Ajax Call
def product_data_gst(request):
    productdata = Product_gst.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def getproducts_gst_sale(request):
    productdata = Product_gst.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def customer_state_gst(request):
    cname = request.GET['cname'] 
    customer = Customer_gst.objects.get(id=Customer_gst.objects.get(fullname=cname).id)
    state = customer.state

    return HttpResponse(state)

def check_stock_gst(request):
    stock = Stock_gst.objects.all()
    return JsonResponse({"stock_data":list(stock.values())})

def sellingprice_gst(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    rate_ = 0
    last_price = 0
    last_rate = 0
    pk_id = 0
    
    if gstsale.objects.filter(customer_name = Customer_gst.objects.get(fullname=cname)).count() >= 1:
        customer_id = gstsale.objects.filter(customer_name = Customer_gst.objects.get(fullname=cname)).last()
        pk_id = customer_id.Bill_no
        
    if gstsales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).count() >= 1:
        product_rate = gstsales_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).last()
        rate_ = product_rate.rate
        print(rate_)
    else:
        last_price = Product_gst.objects.get(product_name=pname).selling_price


    if len(str(rate_)) > 1:
        last_rate = rate_
        print(last_rate)
    else:
        last_rate = last_price
        print(last_rate)

    return HttpResponse(last_rate)

def ownerstate_gst_sale(request):
    state = request.user.profile.state
    print(state)

    return HttpResponse(state)