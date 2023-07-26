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
# Create your views here.
@login_required(login_url='login')
def addproduct(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if "Estimate" in request.POST:
                    product = Product_estimate(
                        product_name = request.POST['productname'],
                        product_categ = request.POST['productcategory'],
                        unit = request.POST['unit'],
                        selling_price = request.POST['sellingprice'],
                        store_location = request.POST['storelocation'],
                        supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier']),
                        minimum_stock =  request.POST['minimum_stock']
                    )
                    product.save()
                    messages.success(request, "Product Addedd Successfully ! ")
                else:
                    product = Product_gst(
                        product_name = request.POST['productname'],
                        product_categ = request.POST['productcategory'],
                        unit = request.POST['unit'],
                        selling_price = request.POST['sellingprice'],
                        store_location = request.POST['storelocation'],
                        supplier = Supplier_gst.objects.get(fullname=request.POST['supplier']),
                        minimum_stock =  request.POST['minimum_stock']
                    )
                    product.save()
                    messages.success(request , "Product Addedd Successfully ! ")

            if Estimate_group in user.groups.all():
                Supplier_data = Supplier_estimate.objects.all()
            if GST_group in user.groups.all():
                Supplier_data = Supplier_gst.objects.all()

            context = {
                'Supplier_data':Supplier_data
            }
            return render(request,"dashboard/addproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def viewproduct(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                Product_data = Product_estimate.objects.all()
            if GST_group in user.groups.all():
                Product_data = Product_gst.objects.all()
            context = {
                'Product_data' : Product_data
            }
            return render(request,"dashboard/viewproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def updateproduct(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method =='POST':
                if Estimate_group in user.groups.all():
                    product = Product_estimate.objects.get(pk=pk)

                    product.product_name = request.POST['productname']
                    product.product_categ = request.POST['productcategory']
                    product.unit  = request.POST['unit']
                    product.selling_price = request.POST['sellingprice']
                    product.store_location = request.POST['storelocation']
                    product.supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier'])
                    product.minimum_stock = request.POST['minimum_stock']
                    product.save()
                    messages.success(request, "Product Updated Successfully ! ")

                if GST_group in user.groups.all():
                    product = Product_gst.objects.get(pk=pk)

                    product.product_name = request.POST['productname']
                    product.product_categ = request.POST['productcategory']
                    product.unit = request.POST['unit']
                    product.selling_price = request.POST['sellingprice']
                    product.store_location = request.POST['storelocation']
                    product.supplier = Supplier_gst.objects.get(fullname=request.POST['supplier'])
                    product.minimum_stock = request.POST['minimum_stock']
                    product.save()
                    messages.success(request , "Product Updated Successfully ! ")
            
            if Estimate_group in user.groups.all():
                Product_data = Product_estimate.objects.get(pk=pk)
                supplier_data = Supplier_estimate.objects.all()
            
            if GST_group in user.groups.all():
                Product_data = Product_gst.objects.get(pk=pk)
                supplier_data = Supplier_gst.objects.all()

            context = {
                'Product_data' : Product_data,
                'supplier_data' :  supplier_data
            }
            return render(request,"dashboard/updateproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def estimatepurchasec(request):
    global epc
    epc=int(request.GET['c'])
    print(epc)
    return HttpResponse(epc)

@login_required(login_url='login')
def gstpurchasec(request):
    global gstp
    gstp=int(request.GET['c'])
    return HttpResponse(gstp)


@login_required(login_url='login')
def addpurchase(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:
                Round_off = request.POST['roff']
                if len(Round_off) >= 1 :
                    Round_off = Round_off
                else:
                    Round_off = 0

                Due_amount = request.POST['oldamt']
                if len(Due_amount) >= 1 :
                    Due_amount = Due_amount
                else:
                    Due_amount = 0

                Estimate = Estimate_Purchase(
                    Bill_no = request.POST['bill_no'],
                    supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier']),
                    Total_amount = request.POST['total'],
                    Due_amount = Due_amount,
                    Round_off = Round_off,
                    Grand_total = request.POST['gtot']
                )
                

                supplierAccount = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(fullname=request.POST['supplier']))
                supplierAccount.amount = float(request.POST['gtot'])
                

                for i in range(0,epc):
                    if len(request.POST['dis'+str(i)]) >= 1:
                        dis = request.POST['dis'+str(i)]
                    else:
                        dis = 0

                    estimate = estimatepurchase_Product (
                        Bill_no = request.POST['bill_no'],
                        product_name = request.POST['prod'+str(i)],
                        unit = request.POST['unit'+str(i)],
                        rate = request.POST['rate'+str(i)],
                        qty = request.POST['qty'+str(i)],
                        dis = dis,
                        netrate = request.POST['nr'+str(i)],
                        total = request.POST['tot'+str(i)]
                    )
                    
                    print("Product Added !")

                    stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                    c = stock.quantity
                    a = int(c)
                    stock.quantity = a + int(request.POST['qty'+str(i)])
                    stock.save()
                    estimate.save()

                Estimate.save()
                supplierAccount.save()
                messages.success(request,"Purchase Added Successfully ! ")

            else:
                if len(request.POST['roff']) >= 1:
                    Round_off = request.POST['roff']
                else:
                    Round_off = 0

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

                GSTPURCHASE = GST_Purchase (
                    Bill_no=request.POST['bill_no'],
                    supplier_name=Supplier_gst.objects.get(fullname=request.POST['supplier']),
                    total_amount=request.POST['total'],
                    CGST=CGST,
                    SGST=SGST,
                    IGST=IGST,
                    Round_off=Round_off,
                    Grand_total=request.POST['gtot']
                )

                

                GSTSUPPLIER = supplieraccount_gst.objects.get(supplier_name = Supplier_gst.objects.get(fullname=request.POST['supplier']))
                GSTSUPPLIER.amount = float(request.POST['gtot']) + float(GSTSUPPLIER.amount)
                

                for i in range(0,gstp):
                    Gstpurchase = gstpurchase_Product (
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
                    stock.quantity = a + b
                    stock.save()
                    Gstpurchase.save()

                GSTPURCHASE.save()
                GSTSUPPLIER.save()

                messages.success(request,"Purchase Added Successfully ! ")

        date_ = date.today()
        d1 = date_.strftime("%d/%m/%Y")

        if Estimate_group in user.groups.all():
            Product_data = Product_estimate.objects.all()
            Supplier_data = Supplier_estimate.objects.all()

            if Estimate_Purchase.objects.all().exists():
                new_bill = Estimate_Purchase.objects.last().Bill_no
                new_bill = new_bill + 1
            else:
                new_bill = 1

        if GST_group in user.groups.all():
            Product_data = Product_gst.objects.all()
            Supplier_data = Supplier_gst.objects.all()

            if GST_Purchase.objects.all().exists():
                new_bill = GST_Purchase.objects.last().Bill_no
                new_bill = new_bill + 1
            else:
                new_bill = 1

        context = {
            'Product_data' : Product_data,
            'Supplier_data' : Supplier_data,
            'new_bill' : new_bill,
            'd1' : d1,
        }
        return render(request,"dashboard/purchase.html",context)
    else:
        return redirect('login')

# Ajax Call views Start here
@login_required(login_url='login')
def supplierdueamount_estimate(request):
    cname = request.GET['cname']
    camount = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(fullname=cname).id)
    due_amount = camount.amount

    return HttpResponse(due_amount)

@login_required(login_url='login')
def purchaseprice_estimate(request):
    pname = request.GET['pname']
    sname = request.GET['sname']
    rate_ = 0
    last_price = 0
    last_rate = 0
    pk_id = 0
    # cname = Estimate_sales.objects.filter(customer = Customer.objects.get(fullname=cname)).last()
    # product = estimatesales_Product.objects.filter(Bill_no=cname.Bill_no)
    # product_rate = estimatesales_Product.objects.get(Bill_no=product,product_name=pname).rate

    # if product_rate:
    #     product_rate = product_rate
    # else:
    #     product_rate = Product.objects.get(product_name=pname).selling_price 
    if Estimate_Purchase.objects.filter(supplier = Supplier_estimate.objects.get(fullname=sname)).count() >= 1:
        customer_id = Estimate_Purchase.objects.filter(supplier = Supplier_estimate.objects.get(fullname=sname)).last()
        pk_id = customer_id.Bill_no
        # products = estimatesales_Product.objects.filter(Bill_no=pk_id).last()

    if estimatepurchase_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).count() >= 1:
        product_rate = estimatepurchase_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).last()
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

    # rate_product = estimatesales_Product.objects.get(product_name=product_rate).rate
    # selling_price = Product.objects.get(product_name=pname).selling_price

    return HttpResponse(last_rate)

@login_required(login_url='login')
def getproducts_estimate(request):
    productdata = Product_estimate.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

# GST Start Here
def supplier_state_gst(request):
    sname = request.GET['sname'] 
    supplier = Supplier_gst.objects.get(id=Supplier_gst.objects.get(fullname=sname).id)
    state = supplier.state

    return HttpResponse(state)

def ownerstate_gst(request):
    state = request.user.profile.state
    print(state)

    return HttpResponse(state)

def purchaseprice_gst(request):
    pname = request.GET['pname']
    sname = request.GET['sname']
    rate_ = 0
    last_price = 0
    last_rate = 0
    pk_id = 0
    # cname = Estimate_sales.objects.filter(customer = Customer.objects.get(fullname=cname)).last()
    # product = estimatesales_Product.objects.filter(Bill_no=cname.Bill_no)
    # product_rate = estimatesales_Product.objects.get(Bill_no=product,product_name=pname).rate

    # if product_rate:
    #     product_rate = product_rate
    # else:
    #     product_rate = Product.objects.get(product_name=pname).selling_price 
    if GST_Purchase.objects.filter(supplier_name = Supplier_gst.objects.get(fullname=sname)).count() >= 1:
        customer_id = GST_Purchase.objects.filter(supplier_name = Supplier_gst.objects.get(fullname=sname)).last()
        pk_id = customer_id.Bill_no
        # products = estimatesales_Product.objects.filter(Bill_no=pk_id).last()

    if gstpurchase_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).count() >= 1:
        product_rate = gstpurchase_Product.objects.filter(product_name=pname).filter(Bill_no=pk_id).last()
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

    # rate_product = estimatesales_Product.objects.get(product_name=product_rate).rate
    # selling_price = Product.objects.get(product_name=pname).selling_price

    return HttpResponse(last_rate)

@login_required(login_url='login')
def viewpurchase(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                Purchase_data = Estimate_Purchase.objects.all()

            if GST_group in user.groups.all():
                Purchase_data = GST_Purchase.objects.all()

            context = {
                'Purchase_data' : Purchase_data
            }
            return render(request,"dashboard/viewpurchase.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def updatepurchase(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:
                Round_off = request.POST['roff']
                if len(Round_off) >= 1 :
                    Round_off = Round_off
                else:
                    Round_off = 0

                Due_amount = request.POST['oldamt']
                if len(Due_amount) >= 1 :
                    Due_amount = Due_amount
                else:
                    Due_amount = 0
                
                old_grant_total =  request.POST['cod']

                purchase_product_count = estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
                bill_product = estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no'])

                for j in range(0,purchase_product_count):
                    print(bill_product[j].product_name)
                    add_stock = Stock_estimate.objects.get(product=Product_estimate.objects.get(product_name=bill_product[j].product_name))
                    add_stock.quantity = add_stock.quantity - bill_product[j].qty
                    add_stock.save()

                Estimate_Purchase.objects.get(Bill_no=request.POST['bill_no']).delete()
                estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

                Estimate = Estimate_Purchase(
                    Bill_no = request.POST['bill_no'],
                    supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier']),
                    Total_amount = request.POST['total'],
                    Due_amount = Due_amount,
                    Round_off = Round_off,
                    Grand_total = request.POST['gtot']
                )
                
                old_amount = float(request.POST['gtot']) - float(old_grant_total) 

                supplierAccount = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(fullname=request.POST['supplier']))
                supplierAccount.amount = float(supplierAccount.amount) + float(old_amount)
                
                for i in range(0,epc):
                    if len(request.POST['dis'+str(i)]) >= 1:
                        dis = request.POST['dis'+str(i)]
                    else:
                        dis = 0

                    estimate = estimatepurchase_Product (
                        Bill_no = request.POST['bill_no'],
                        product_name = request.POST['prod'+str(i)],
                        unit = request.POST['unit'+str(i)],
                        rate = request.POST['rate'+str(i)],
                        qty = request.POST['qty'+str(i)],
                        dis = dis,
                        netrate = request.POST['nr'+str(i)],
                        total = request.POST['tot'+str(i)]
                    )
                    
                    print("Product Added !")

                    stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                    c = stock.quantity
                    a = int(c)
                    stock.quantity = a + int(request.POST['qty'+str(i)])
                    stock.save()
                    estimate.save()

                Estimate.save()
                supplierAccount.save()
                
                return redirect('viewpurchase')
                messages.success(request,"Purchase Successfully !")

            if 'GST' in request.POST:

                if len(request.POST['roff']) >= 1:
                    Round_off = request.POST['roff']
                else:
                    Round_off = 0

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

                purchase_product_count = gstpurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
                bill_product = gstpurchase_Product.objects.filter(Bill_no=request.POST['bill_no'])

                for j in range(0,purchase_product_count):
                    print(bill_product[j].product_name)
                    add_stock = Stock_gst.objects.get(product=Product_gst.objects.get(product_name=bill_product[j].product_name))
                    add_stock.quantity = add_stock.quantity - bill_product[j].qty
                    add_stock.save()

                GST_Purchase.objects.get(Bill_no=request.POST['bill_no']).delete()
                gstpurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

                GSTPURCHASE = GST_Purchase (
                    Bill_no=request.POST['bill_no'],
                    supplier_name = Supplier_gst.objects.get(fullname = request.POST['supplier']),
                    total_amount=request.POST['total'],
                    CGST=CGST,
                    SGST=SGST,
                    IGST=IGST,
                    Round_off=Round_off,
                    Grand_total=request.POST['gtot']
                )

                old_amount = float(request.POST['gtot']) - float(old_grant_total)

                GSTSUPPLIER = supplieraccount_gst.objects.get(supplier_name = Supplier_gst.objects.get(fullname=request.POST['supplier']))
                GSTSUPPLIER.amount = float(GSTSUPPLIER.amount) + float(old_amount)

                for i in range(0,gstp):
                    Gstpurchase = gstpurchase_Product (
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
                    stock.quantity = a + b
                    stock.save()

                Gstpurchase.save()
                GSTSUPPLIER.save()
                GSTPURCHASE.save()

                return redirect('viewpurchase')
                messages.success(request,"Purchase Successfully !")

        if Estimate_group in user.groups.all():
            purchase_Bill_no = Estimate_Purchase.objects.get(pk=pk).Bill_no
            purchase_Bill_date = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no).date
            purchase_data = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no)
            purchase_product = estimatepurchase_Product.objects.filter(Bill_no=purchase_Bill_no)
            supplier_data = Supplier_estimate.objects.all()
            product_data = Product_estimate.objects.all()

        if GST_group in user.groups.all():
            purchase_Bill_no = GST_Purchase.objects.get(pk=pk).Bill_no
            purchase_Bill_date = GST_Purchase.objects.get(pk=pk).date
            purchase_data = GST_Purchase.objects.get(Bill_no=purchase_Bill_no)
            purchase_product = gstpurchase_Product.objects.filter(Bill_no=purchase_Bill_no)
            supplier_data = Supplier_gst.objects.all()
            product_data = Product_gst.objects.all()
        
        context = {
            'purchase_Bill_no' : purchase_Bill_no,
            'purchase_data' : purchase_data,
            'purchase_product' : purchase_product,
            'supplier_data' : supplier_data,
            'product_data' : product_data,
            'purchase_Bill_date':purchase_Bill_date,
        }
        return render(request,"dashboard/updatepurchase.html",context)
    else:
        return redirect('login')


@login_required(login_url='login')
def purchaseinvoice(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if Estimate_group in user.groups.all():
            Purchase_data = Estimate_Purchase.objects.get(pk=pk)
            Purchase_data_product = estimatepurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
            word = 1

        if GST_group in user.groups.all():
            Purchase_data = GST_Purchase.objects.get(pk=pk)
            Purchase_data_product = gstpurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
            word =num2words(gst.Grand_total)

        raw_text = u"\u20B9"
        print(raw_text)

        context = {
            'Purchase_data' : Purchase_data,
            'Purchase_data_product' : Purchase_data_product,
            'word' : word
        }
        return render(request,"dashboard/purchaseinvoice.html",context)
    else:
        return redirect('login')

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
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:
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
                    customer = Customer_estimate.objects.get(id = Customer_estimate.objects.get(fullname=request.POST['customer']).id),
                    Total_amount=request.POST['total'],
                    Due_amount=request.POST['oldamt'],
                    Round_off=Round_off,
                    Grand_total=request.POST['gtot']
                )

                customerAccount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']))
                customerAccount.amount = float(Grand_total)
                customerAccount.save()
                
                if cash_on_hand == 0:
                    print("Customer Payment")
                else:
                    CustomerPay = customerpay_estimate (
                        customer_name = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']).id).customer_name,
                        pending_amount = Grand_total,
                        paid_amount = cash_on_hand,
                        round_off = 0
                    )
                    CustomerPay.save()

                customerdata = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']).id)
                pendingamount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']).id).amount
                customerdata.amount  = float(pendingamount) - float(cash_on_hand)
                

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
                customerdata.save()

            # esti_id = Estimate_sales.objects.all().last().pk
            # return redirect('/dashboard/saleinvoice/'+str(esti_id))

            if 'GST' in request.POST:
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

            # gst_id = gstsale.objects.all().last().pk
            # return redirect('/dashboard/saleinvoice/'+str(gst_id))

        date_ = date.today()
        d1 = date_.strftime("%d/%m/%Y")

        if Estimate_group in user.groups.all():
            Product_data = Product_estimate.objects.all()
            Customer_data = Customer_estimate.objects.all()
    
            if Estimate_sales.objects.all().exists():
                new_billno = Estimate_sales.objects.last().Bill_no
                new_billno = new_billno + 1
            else:
                new_billno = 1
        
        if GST_group in user.groups.all():
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
        return render(request,"dashboard/sale.html",context)
    else:
        return redirect('login')

@login_required(login_url='login')
def viewsale(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if Estimate_group in user.groups.all():
            Sale_data = Estimate_sales.objects.all()

        if GST_group in user.groups.all():
            Sale_data = gstsale.objects.all()

        context = {
            'Sale_data' : Sale_data
        }
        return render(request,"dashboard/viewsale.html",context)
    else:
        return redirect('login')

@login_required(login_url='login')
def updatesale(request , pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:
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

            if 'GST' in request.POST:

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


        if Estimate_group in user.groups.all():
            sale_Bill_no = Estimate_sales.objects.get(pk=pk).Bill_no
            sale_data = Estimate_sales.objects.get(Bill_no=sale_Bill_no)
            sale_product = estimatesales_Product.objects.filter(Bill_no=sale_Bill_no)
            customer_data = Customer_estimate.objects.all()
            product_data = Product_estimate.objects.all()


        if GST_group in user.groups.all():
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
        return render(request,"dashboard/updatesale.html",context)
    else:
        return redirect('login')

@login_required(login_url='login')
def saleinvoice(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                sale_data = Estimate_sales.objects.get(pk=pk)
                product_data = estimatesales_Product.objects.filter(Bill_no = sale_data.Bill_no)
                word = 1

            if GST_group in user.groups.all():
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
            return render(request,"dashboard/saleinvoice.html",context)
        else:
            return redirect('login')
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
    # cname = Estimate_sales.objects.filter(customer = Customer.objects.get(fullname=cname)).last()
    # product = estimatesales_Product.objects.filter(Bill_no=cname.Bill_no)
    # product_rate = estimatesales_Product.objects.get(Bill_no=product,product_name=pname).rate

    # if product_rate:
    #     product_rate = product_rate
    # else:
    #     product_rate = Product.objects.get(product_name=pname).selling_price 
    if Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(fullname=cname)).count() >= 1:
        customer_id = Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(fullname=cname)).last()
        pk_id = customer_id.Bill_no
        # products = estimatesales_Product.objects.filter(Bill_no=pk_id).last()

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

    # rate_product = estimatesales_Product.objects.get(product_name=product_rate).rate
    # selling_price = Product.objects.get(product_name=pname).selling_price

    return HttpResponse(last_rate)

def product_data_estimate(request):
    productdata = Product_estimate.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def stock_data_estimate(request):
    stock_data = Stock_estimate.objects.all()
    return JsonResponse({"stock_data":list(stock_data.values())})

def stock_data_gst(request):
    stock_data = Stock_gst.objects.objects.all()
    return JsonResponse({"stock_data":list(stock_data.values())})

@login_required(login_url='login')
def previous_discount_estimate(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    rate_ = 0
    last_price = 0
    last_discount = 0
    pk_id = 0
    # cname = Estimate_sales.objects.filter(customer = Customer.objects.get(fullname=cname)).last()
    # product = estimatesales_Product.objects.filter(Bill_no=cname.Bill_no)
    # product_rate = estimatesales_Product.objects.get(Bill_no=product,product_name=pname).rate

    # if product_rate:
    #     product_rate = product_rate
    # else:
    #     product_rate = Product.objects.get(product_name=pname).selling_price 
    if Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(fullname=cname)).count() >= 1:
        customer_id = Estimate_sales.objects.filter(customer = Customer_estimate.objects.get(fullname=cname)).last()
        pk_id = customer_id.Bill_no
        # products = estimatesales_Product.objects.filter(Bill_no=pk_id).last()

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

    # rate_product = estimatesales_Product.objects.get(product_name=product_rate).rate
    # selling_price = Product.objects.get(product_name=pname).selling_price

    return HttpResponse(last_discount)

@login_required(login_url='login')
def customerdue_estimate(request):
    cname = request.GET['cname']
    camount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=cname).id)
    due_amount = camount.amount

    return HttpResponse(due_amount)

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
    # cname = Estimate_sales.objects.filter(customer = Customer.objects.get(fullname=cname)).last()
    # product = estimatesales_Product.objects.filter(Bill_no=cname.Bill_no)
    # product_rate = estimatesales_Product.objects.get(Bill_no=product,product_name=pname).rate

    # if product_rate:
    #     product_rate = product_rate
    # else:
    #     product_rate = Product.objects.get(product_name=pname).selling_price 
    if gstsale.objects.filter(customer_name = Customer_gst.objects.get(fullname=cname)).count() >= 1:
        customer_id = gstsale.objects.filter(customer_name = Customer_gst.objects.get(fullname=cname)).last()
        pk_id = customer_id.Bill_no
        # products = estimatesales_Product.objects.filter(Bill_no=pk_id).last()

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

    # rate_product = estimatesales_Product.objects.get(product_name=product_rate).rate
    # selling_price = Product.objects.get(product_name=pname).selling_price

    return HttpResponse(last_rate)

def ownerstate_gst_sale(request):
    state = request.user.profile.state
    print(state)

    return HttpResponse(state)

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