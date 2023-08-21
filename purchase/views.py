from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from products.models import *

from .models import *

# Create your views here.
@login_required(login_url='login')
def addpurchase(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
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

        if request.user.groups.filter(name='GST').exists():
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

    if request.user.groups.filter(name='Estimate').exists():
        Product_data = Product_estimate.objects.all()
        Supplier_data = Supplier_estimate.objects.all()

        if Estimate_Purchase.objects.all().exists():
            new_bill = Estimate_Purchase.objects.all().count()
            new_bill = new_bill + 1
        else:
            new_bill = 1

    if request.user.groups.filter(name='GST').exists():
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
    return render(request,"purchase/purchase.html",context)
    
@login_required(login_url='login')
def viewpurchase(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            Purchase_data = Estimate_Purchase.objects.all()

        if request.user.groups.filter(name='GST').exists():
            Purchase_data = GST_Purchase.objects.all()

        context = {
            'Purchase_data' : Purchase_data
        }
        return render(request,"purchase/viewpurchase.html",context)
    except:
        return redirect('error404')
    
@login_required(login_url='login')
def updatepurchase(request,pk):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
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

        if request.user.groups.filter(name='GST').exists():
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

    if request.user.groups.filter(name='Estimate').exists():
        purchase_Bill_no = Estimate_Purchase.objects.get(pk=pk).Bill_no
        purchase_Bill_date = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no).date
        purchase_data = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no)
        purchase_product = estimatepurchase_Product.objects.filter(Bill_no=purchase_Bill_no)
        supplier_data = Supplier_estimate.objects.all()
        product_data = Product_estimate.objects.all()

    if request.user.groups.filter(name='GST').exists():
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
    return render(request,"purchase/updatepurchase.html",context)
    
@login_required(login_url='login')
def purchaseinvoice(request,pk):
    if request.user.groups.filter(name='Estimate').exists():
        Purchase_data = Estimate_Purchase.objects.get(pk=pk)
        Purchase_data_product = estimatepurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
        word = 1

    if request.user.groups.filter(name='GST').exists():
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
    return render(request,"purchase/purchaseinvoice.html",context)
    
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
    
    if Estimate_Purchase.objects.filter(supplier = Supplier_estimate.objects.get(fullname=sname)).count() >= 1:
        customer_id = Estimate_Purchase.objects.filter(supplier = Supplier_estimate.objects.get(fullname=sname)).last()
        pk_id = customer_id.Bill_no

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

    return HttpResponse(last_rate)

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
    
    if GST_Purchase.objects.filter(supplier_name = Supplier_gst.objects.get(fullname=sname)).count() >= 1:
        customer_id = GST_Purchase.objects.filter(supplier_name = Supplier_gst.objects.get(fullname=sname)).last()
        pk_id = customer_id.Bill_no

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

    return HttpResponse(last_rate)