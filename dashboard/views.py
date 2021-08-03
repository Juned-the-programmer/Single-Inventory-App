from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from .models import *
from pages.models import *
from django.contrib import messages
from django.http import  HttpResponse , JsonResponse
from datetime import date
from num2words import num2words
# Create your views here.
customerid_estimate = 1
customerid_gst = 1
@login_required(login_url='login')
def addcustomer(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                global customerid_estimate
                global customerid_gst
                if 'Estimate' in request.POST:
                    customer = Customer_estimate(
                        customerid = request.POST['customerid'],
                        fullname = request.POST['fullname'],
                        contactno = request.POST['mobile'],
                        city = request.POST['city'],
                        state = request.POST['state'],
                        landmark = request.POST['landmark']
                    )
                    customer.save()
                    messages.success(request , "Added Customer Successfully ! ")
                else:
                    customer = Customer_gst(
                        customerid = request.POST['customerid'],
                        fullname = request.POST['fullname'],
                        email = request.POST['email'],
                        contactno = request.POST['mobile'],
                        gst = request.POST['gstno'],
                        city = request.POST['city'],
                        state = request.POST['state'],
                        landmark = request.POST['landmark']
                    )
                    customer.save()
                    messages.success(request, "Added Customer Successfully ! ")

            if Estimate_group in user.groups.all():
                if Customer_estimate.objects.all().exists():
                    customerdata_estimate = Customer_estimate.objects.last().customerid
                    customerid_estimate = customerdata_estimate + 1
                else:
                    customerid_estimate = 1

            if GST_group in user.groups.all():
                if Customer_gst.objects.all().exists():
                    customerdata_gst = Customer_gst.objects.last().customerid
                    customerid_gst = customerdata_gst + 1
                else:
                    customerid_gst = 1
            
            context = {
                'customerid_estimate' : customerid_estimate,
                'customerid_gst' : customerid_gst
            }
            return render(request,"dashboard/addcustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')


customerdata_estimate = 1
customerdata_gst = 1
@login_required(login_url='login')
def viewcustomer(request):
    global customerdata_estimate
    global customerdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                customerdata_estimate = Customer_estimate.objects.all()
            
            if GST_group in user.groups.all():
                customerdata_gst = Customer_gst.objects.all()

            context = {
                'customerdata_estimate' : customerdata_estimate,
                'customerdata_gst' : customerdata_gst
            }
            return render(request,"dashboard/viewcustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

customerdata_gst = 1
customerdata_estimate = 1 
@login_required(login_url='login')
def updatecustomer(request,pk):
    global customerdata_estimate
    global customerdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    customer = Customer_estimate.objects.get(pk=pk)

                    customer.fullname = request.POST['fullname']
                    customer.customerid = request.POST['customerid']
                    customer.contactno = request.POST['mobile']
                    customer.city = request.POST['city']
                    customer.state = request.POST['state']
                    customer.landmark = request.POST['landmark']

                    customer.save()
                    messages.success(request,"Update Customer Successfully ! ")
                else:
                    customer = Customer_gst.objects.get(pk=pk)

                    customer.fullname = request.POST['fullname']
                    customer.customerid = request.POST['customerid']
                    customer.contactno = request.POST['mobile']
                    customer.gst = request.POST['gstno']
                    customer.email = request.POST['email']
                    customer.city = request.POST['city']
                    customer.state = request.POST['state']
                    customer.landmark = request.POST['landmark']

                    customer.save()
                    messages.success(request, "Update Customer Successfully ! ")

            # if user.groups.filter(name=Estimate_group):
            #     print("Estimate")
            #     customerdata_estimate = Customer_estimate.objects.get(pk=pk)
            # else:
            #     print("No Estimate data")

            # if user.groups.filter(name=GST_group):
            #     print("GST")
            #     customerdata_gst = Customer_gst.objects.get(pk=pk)
            # else:
            #     print("No GST data")
            # customerdata_gst =  Customer_gst.objects.get(pk=pk) 

            if Estimate_group in user.groups.all():
                customerdata_gst == 1
                print(customerdata_gst)
                customerdata_estimate = Customer_estimate.objects.get(pk=pk)


            if GST_group in user.groups.all():
                customerdata_gst = Customer_gst.objects.get(pk=pk)
                customerdata_estimate == 1
                print(customerdata_estimate)

            context = {
                'customerdata_estimate' : customerdata_estimate,
                'customerdata_gst' : customerdata_gst
            }
            return render(request,"dashboard/updatecustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def addsupplier(request):
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    supplier = Supplier_estimate(
                        supplierid = request.POST['supplierid'],
                        fullname = request.POST['fullname'],
                        contactno = request.POST['mobile'],
                        city = request.POST['city'],
                        state = request.POST['state'],
                        landmark = request.POST['landmark']
                    )
                    supplier.save()
                    messages.success(request , "Added Supplier Successfully ! ")
                else:
                    supplier = Supplier_gst(
                        supplierid = request.POST['supplierid'],
                        fullname = request.POST['fullname'],
                        email = request.POST['email'],
                        contactno = request.POST['mobile'],
                        gst = request.POST['gstno'],
                        city = request.POST['city'],
                        state = request.POST['state'],
                        landmark = request.POST['landmark']
                    )
                    supplier.save()
                    messages.success(request, "Added Supplier Successfully ! ")

            if Supplier_estimate.objects.all().exists():
                supplierdata_estimate = Supplier_estimate.objects.last().supplierid
                supplierid_estimate = supplierdata_estimate + 1
            else:
                supplierid_estimate = 1

            if Supplier_gst.objects.all().exists():
                supplierdata_gst = Supplier_gst.objects.last().supplierid
                supplierid_gst = supplierdata_gst + 1
            else:
                supplierid_gst = 1
            
            context = {
                'supplierid_estimate' : supplierid_estimate,
                'supplierid_gst' : supplierid_gst
            }
            return render(request,"dashboard/addsupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

supplierdata_estimate = 1
supplierdata_gst = 1
@login_required(login_url='login')
def viewsupplier(request):
    global supplierdata_estimate
    global supplierdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                supplierdata_estimate = Supplier_estimate.objects.all()
            if GST_group in user.groups.all():
                supplierdata_gst = Supplier_gst.objects.all()

            context = {
                'supplierdata_estimate' : supplierdata_estimate,
                'supplierdata_gst' : supplierdata_gst
            }
            return render(request,"dashboard/viewsupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

supplierdata_estimate = 1
supplierdata_gst = 1
@login_required(login_url='login')
def updatesupplier(request,pk):
    global supplierdata_estimate
    global supplierdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    supplier = Supplier_estimate.objects.get(pk=pk)

                    supplier.fullname = request.POST['fullname']
                    supplier.customerid = request.POST['customerid']
                    supplier.contactno = request.POST['mobile']
                    supplier.city = request.POST['city']
                    supplier.state = request.POST['state']
                    supplier.landmark = request.POST['landmark']

                    supplier.save()
                    messages.success(request,"Update Supplier Successfully ! ")
                else:
                    supplier = Supplier_gst.objects.get(pk=pk)

                    supplier.fullname = request.POST['fullname']
                    supplier.customerid = request.POST['customerid']
                    supplier.contactno = request.POST['mobile']
                    supplier.gst = request.POST['gstno']
                    supplier.email = request.POST['email']
                    supplier.city = request.POST['city']
                    supplier.state = request.POST['state']
                    supplier.landmark = request.POST['landmark']

                    supplier.save()
                    messages.success(request, "Update Supplier Successfully ! ")

            # if user.groups.filter(name=Estimate_group):
            #     print("Estimate")
            #     customerdata_estimate = Customer_estimate.objects.get(pk=pk)
            # else:
            #     print("No Estimate data")

            # if user.groups.filter(name=GST_group):
            #     print("GST")
            #     customerdata_gst = Customer_gst.objects.get(pk=pk)
            # else:
            #     print("No GST data")
            # customerdata_gst =  Customer_gst.objects.get(pk=pk) 

            if Estimate_group in user.groups.all():
                supplierdata_gst == 1
                print(supplierdata_gst)
                supplierdata_estimate = Supplier_estimate.objects.get(pk=pk)


            if GST_group in user.groups.all():
                supplierdata_gst = Supplier_gst.objects.get(pk=pk)
                supplierdata_estimate == 1
                print(supplierdata_estimate)

            context = {
                'supplierdata_estimate' : supplierdata_estimate,
                'supplierdata_gst' : supplierdata_gst
            }
            return render(request,"dashboard/updatesupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

supplierdata_estimate = 1
supplierdata_gst = 1
@login_required(login_url='login')
def addproduct(request):
    global supplierdata_estimate
    global supplierdata_gst
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
                supplierdata_estimate = Supplier_estimate.objects.all()
            if GST_group in user.groups.all():
                supplierdata_gst = Supplier_gst.objects.all()

            context = {
                'supplierdata_estimate' : supplierdata_estimate,
                'supplierdata_gst' : supplierdata_gst
            }
            return render(request,"dashboard/addproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

productdata_estimate = 1
productdata_gst = 1
@login_required(login_url='login')
def viewproduct(request):
    global productdata_estimate
    global productdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                productdata_estimate = Product_estimate.objects.all()
            if GST_group in user.groups.all():
                productdata_gst = Product_gst.objects.all()
            context = {
                'productdata_estimate' : productdata_estimate,
                'productdata_gst' : productdata_gst
            }
            return render(request,"dashboard/viewproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

productdata_estimate = 1
productdata_gst = 1
@login_required(login_url='login')
def updateproduct(request,pk):
    global productdata_estimate
    global productdata_gst
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
                productdata_estimate = Product_estimate.objects.get(pk=pk)
                print(productdata_estimate)
                productdata_gst = 1
            
            if GST_group in user.groups.all():
                productdata_gst = Product_gst.objects.get(pk=pk)
                print(productdata_gst)
                productdata_estimate = 1

            context = {
                'productdata_estimate' : productdata_estimate,
                'productdata_gst' : productdata_gst
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

productdata_estimate = 1
productdata_gst = 1
supplierdata_estimate = 1
supplierdata_gst = 1
estimate_newbillno = 1
gst_newbillno = 1
@login_required(login_url='login')
def addpurchase(request):
    global productdata_estimate
    global productdata_gst
    global supplierdata_estimate
    global supplierdata_gst
    global estimate_newbillno
    global gst_newbillno
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
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
                    Estimate.save()

                    supplierAccount = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(fullname=request.POST['supplier']))
                    supplierAccount.amount = float(request.POST['gtot'])
                    supplierAccount.save()

                    for i in range(0,epc):
                        estimate = estimatepurchase_Product (
                            Bill_no = request.POST['bill_no'],
                            product_name = request.POST['prod'+str(i)],
                            unit = request.POST['unit'+str(i)],
                            rate = request.POST['rate'+str(i)],
                            qty = request.POST['qty'+str(i)],
                            dis = request.POST['dis'+str(i)],
                            netrate = request.POST['nr'+str(i)],
                            total = request.POST['tot'+str(i)]
                        )
                        estimate.save()
                        print("Product Added !")

                        stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                        c = stock.quantity
                        a = int(c)
                        stock.quantity = a + int(request.POST['qty'+str(i)])
                        stock.save()
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
                        supplier_name=Supplier_gst.objects.get(supplier_name=request.POST['supplier']),
                        total_amount=request.POST['total'],
                        CGST=CGST,
                        SGST=SGST,
                        IGST=IGST,
                        Round_off=Round_off,
                        Grand_total=request.POST['gtot']
                    )

                    GSTPURCHASE.save()

                    GSTSUPPLIER = supplieraccount_gst.objects.get(supplier_name = Supplier_gst.objects.get(fullname=request.POST['supplier']))
                    GSTSUPPLIER.amount = float(request.POST['gtot']) + float(GSTSUPPLIER.amount)
                    GSTSUPPLIER.save()

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
                    messages.success(request,"Purchase Added Successfully ! ")

            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")

            if Estimate_group in user.groups.all():
                productdata_estimate = Product_estimate.objects.all()
                supplierdata_estimate = Supplier_estimate.objects.all()
                productdata_gst = 1
                supplierdata_gst = 1

                if Estimate_Purchase.objects.all().exists():
                    estimate_newbill = Estimate_Purchase.objects.last().Bill_no
                    estimate_newbillno = estimate_newbill + 1
                else:
                    estimate_newbillno = 1

            if GST_group in user.groups.all():
                productdata_gst = Product_gst.objects.all()
                supplierdata_gst = Supplier_gst.objects.all()
                productdata_estimate = 1
                supplierdata_estimate = 1

                if GST_Purchase.objects.all().exists():
                    gst_newbillno = GST_Purchase.objects.last().Bill_no
                    gst_newbillno = gst_newbillno + 1
                else:
                    gst_newbillno = 1

            context = {
                'productdata_estimate' : productdata_estimate,
                'supplierdata_estimate' : supplierdata_estimate,
                'estimate_newbillno' : estimate_newbillno,
                'd1' : d1,
                'productdata_gst' : productdata_gst,
                'supplierdata_gst' : supplierdata_gst,
                'gst_newbillno' : gst_newbillno
            }
            return render(request,"dashboard/purchase.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

# Ajax Call views Start here
@login_required(login_url='login')
def supplierdueamount_estimate(request):
    cname = request.GET['cname']
    camount = supplieraccount_estimate.objects.get(id = Supplier_estimate.objects.get(fullname=cname).id)
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

@login_required(login_url='login')
def punit(request):
    pname=request.GET['pname']
    unit = Product_estimate.objects.get(id=Product_estimate.objects.get(product_name=pname).id)
    p_unit = unit.unit
    return HttpResponse(p_unit)

# GST Start Here
def getproducts_gst(request):
    productdata = Product_gst.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def punit_gst(request):
    pname=request.GET['pname']
    unit = Product_gst.objects.get(id=Product_gst.objects.get(product_name=pname).id)
    p_unit = unit.unit
    return HttpResponse(p_unit)

def supplier_state_gst(request):
    sname = request.GET['sname'] 
    supplier = Supplier_gst.objects.get(id=Supplier_gst.objects.get(fullname=sname).id)
    state = supplier.state
    profile_state_purchase = request.user.profile.state

    return HttpResponse(state,profile_state_purchase)

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

estimate_purchase = 1
gst_purchase = 1
@login_required(login_url='login')
def viewpurchase(request):
    global estimate_purchase
    global gst_purchase
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                estimate_purchase = Estimate_Purchase.objects.all()

            if GST_group in user.groups.all():
                gst_purchase = GST_Purchase.objects.all()

            context = {
                'estimate_purchase': estimate_purchase,
                'gst_purchase' : gst_purchase
            }
            return render(request,"dashboard/viewpurchase.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

purchase_Bill_no = 1
purchase_estimate = 1
purchase_product = 1
supplierdata_estimate = 1
productdata_estimate = 1
@login_required(login_url='login')
def updatepurchase(request,pk):
    global purchase_Bill_no
    global purchase_estimate
    global purchase_product
    global supplierdata_estimate
    global productdata_estimate
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
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
                    Estimate.save()

                    old_amount = float(request.POST['gtot']) - float(old_grant_total) 

                    supplierAccount = supplieraccount_estimate.objects.get(supplier_name = Supplier_estimate.objects.get(fullname=request.POST['supplier']))
                    supplierAccount.amount = float(supplierAccount.amount) + float(old_amount)
                    supplierAccount.save()

                    for i in range(0,epc):
                        estimate = estimatepurchase_Product (
                            Bill_no = request.POST['bill_no'],
                            product_name = request.POST['prod'+str(i)],
                            unit = request.POST['unit'+str(i)],
                            rate = request.POST['rate'+str(i)],
                            qty = request.POST['qty'+str(i)],
                            dis = request.POST['dis'+str(i)],
                            netrate = request.POST['nr'+str(i)],
                            total = request.POST['tot'+str(i)]
                        )
                        estimate.save()
                        print("Product Added !")

                        stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                        c = stock.quantity
                        a = int(c)
                        stock.quantity = a + int(request.POST['qty'+str(i)])
                        stock.save()

                    return redirect('viewpurchase')
                    messages.success(request,"Purchase Successfully !")

            if Estimate_group in user.groups.all():
                purchase_Bill_no = Estimate_Purchase.objects.get(pk=pk).Bill_no
                purchase_estimate = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no)
                purchase_product = estimatepurchase_Product.objects.filter(Bill_no=purchase_Bill_no)
                supplierdata_estimate = Supplier_estimate.objects.all()
                productdata_estimate = Product_estimate.objects.all()

            if GST_group in user.groups.all():
                print('Nothing')
            
            context = {
                'purchase_Bill_no' : purchase_Bill_no,
                'purchase_estimate' : purchase_estimate,
                'purchase_product' : purchase_product,
                'supplierdata_estimate' : supplierdata_estimate,
                'productdata_estimate' : productdata_estimate
            }
            return render(request,"dashboard/updatepurchase.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

estimate = 1
product = 1
gst = 1
product_gst = 1
word = 1
profile_info = 1
@login_required(login_url='login')
def purchaseinvoice(request,pk):
    global estimate
    global product
    global gst
    global product_gst
    global word
    global profile_info
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                estimate = Estimate_Purchase.objects.get(pk=pk)
                product = estimatepurchase_Product.objects.filter(Bill_no = estimate.Bill_no)

            if GST_group in user.groups.all():
                gst = GST_Purchase.objects.get(pk=pk)
                product_gst = gstpurchase_Product.objects.filter(Bill_no = gst.Bill_no)
                word =num2words(gst.Grand_total)

            raw_text = u"\u20B9"
            print(raw_text)

            context = {
                'estimate' : estimate,
                'product' : product,
                'raw_text' : raw_text,
                'gst' : gst,
                'product_gst' : product_gst,
                'word' : word,
                'profile_info' : profile_info
            }
            return render(request,"dashboard/purchaseinvoice.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

def estimatesalec(request):
    global esc
    esc=int(request.GET['c'])
    return HttpResponse(esc)

def gstsalec(request):
    global gst
    gst=int(request.GET['c'])
    return HttpResponse(gst)

productdata_estimate = 1
customerdata_estimate = 1
estimate_newbillno = 1
productdata_gst = 1
customerdata_gst = 1
gst_newbillno = 1
@login_required(login_url='login')
def addsale(request):
    global productdata_estimate
    global customerdata_estimate
    global estimate_newbillno
    global productdata_gst
    global customerdata_gst
    global gst_newbillno
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
                    Round_off = Round_off
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
                Estimatesale.save()

                customerAccount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']))
                customerAccount.amount = float(Grand_total)
                customerAccount.save()
                
                if cash_on_hand == 0:
                    print('Cash on hand is 0')
                else:
                    CustomerPay = customerpay_estimate (
                        customer_name = customeraccount_estimate.objects.get(id = Customer_estimate.objects.get(fullname=request.POST['customer']).id).customer_name,
                        pending_amount = Grand_total,
                        paid_amount = cash_on_hand
                    )
                    CustomerPay.save()
                    print("nothing")

                customerdata = customeraccount_estimate.objects.get(id=Customer_estimate.objects.get(fullname=request.POST['customer']).id)
                pendingamount = customeraccount_estimate.objects.get(id=Customer_estimate.objects.get(fullname=request.POST['customer']).id).amount
                customerdata.amount  = float(pendingamount) - float(cash_on_hand)
                customerdata.save()

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
                GSTSALE.save()

                GSTCUSTOMER = customeraccount_gst.objects.get(customer_name = Customer_gst.objects.get(fullname=request.POST['customer']))
                GSTCUSTOMER.amount = float(GSTCUSTOMER.amount) + float(request.POST['gtot'])
                GSTCUSTOMER.save()

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

            # gst_id = gstsale.objects.all().last().pk
            # return redirect('/dashboard/saleinvoice/'+str(gst_id))

        date_ = date.today()
        d1 = date_.strftime("%d/%m/%Y")

        if Estimate_group in user.groups.all():
            productdata_estimate = Product_estimate.objects.all()
            customerdata_estimate = Customer_estimate.objects.all()
    
            if Estimate_sales.objects.all().exists():
                estimate_newbill = Estimate_sales.objects.last().Bill_no
                estimate_newbillno = estimate_newbill + 1
            else:
                estimate_newbillno = 1
        
        if GST_group in user.groups.all():
            productdata_gst = Product_gst.objects.all()
            customerdata_gst = Customer_gst.objects.all()
            
            if gstsale.objects.all().exists():
                gst_newbill = gstsale.objects.last().Bill_no
                gst_newbillno = gst_newbill + 1
            else:
                gst_newbillno = 1

        context = {
            'productdata_estimate' : productdata_estimate,
            'customerdata_estimate' : customerdata_estimate,
            'estimate_newbillno' : estimate_newbillno,
            'productdata_gst' : productdata_gst,
            'customerdata_gst' : customerdata_gst,
            'gst_newbillno' : gst_newbillno,
            'd1' : d1,
        }
        return render(request,"dashboard/sale.html",context)
    else:
        return redirect('login')

estimate_sales = 1
gst_sales = 1
@login_required(login_url='login')
def viewsale(request):
    global estimate_sales
    global gst_sales
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if Estimate_group in user.groups.all():
            estimate_sales = Estimate_sales.objects.all()

        if GST_group in user.groups.all():
            gst_sales = gstsale.objects.all()

        context = {
            'estimate_sales': estimate_sales,
            'gst_sales' : gst_sales,
        }
        return render(request,"dashboard/viewsale.html",context)
    else:
        return redirect('login')

sale_Bill_no = 1
sale_estimate = 1
sale_product = 1
customerdata_estimate = 1
productdata_estimate = 1
@login_required(login_url='login')
def updatesale(request , pk):
    global sale_Bill_no
    global sale_estimate
    global sale_product
    global customerdata_estimate
    global productdata_estimate
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if Estimate_group in user.groups.all():
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
                    Estimatesale.save()

                    old_amount = float(Grand_total) - float(old_grant_total) 

                    customerAccount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']))
                    customerAccount.amount = float(customerAccount.amount) + float(old_amount) 
                    customerAccount.save()

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

                        estimate.save()

                        stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                        c = stock.quantity
                        a = int(c)
                        b = int(request.POST['qty'+str(i)])
                        stock.quantity = a - b
                        stock.save()
                    
                    return redirect('viewsale')
                    messages.success(request, "Sale Updated Successfully ! ")

            if Estimate_group in user.groups.all():
                sale_Bill_no = Estimate_sales.objects.get(pk=pk).Bill_no
                sale_estimate = Estimate_sales.objects.get(Bill_no=sale_Bill_no)
                sale_product = estimatesales_Product.objects.filter(Bill_no=sale_Bill_no)
                customerdata_estimate = Customer_estimate.objects.all()
                productdata_estimate = Product_estimate.objects.all()


            if GST_group in user.groups.all():
                print("Nothing")

            context = {
                'sale_Bill_no' : sale_Bill_no,
                'sale_estimate' : sale_estimate,
                'sale_product' : sale_product,
                'customerdata_estimate' : customerdata_estimate,
                'productdata_estimate' : productdata_estimate
            }
            return render(request,"dashboard/updatesale.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

estimate = 1   
product = 1     
raw_text = 1
sale = 1
gst = 1
product_gst = 1
word = 1
@login_required(login_url='login')
def saleinvoice(request,pk):
    global estimate
    global product
    global raw_text
    global sale
    global gst
    global product_gst
    global word
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                estimate = Estimate_sales.objects.get(pk=pk)
                product = estimatesales_Product.objects.filter(Bill_no = estimate.Bill_no)

            if GST_group in user.groups.all():
                gst = gstsale.objects.get(pk=pk)
                product_gst = gstsales_Product.objects.filter(Bill_no = gst.Bill_no)
                word =num2words(gst.Grand_total)

            raw_text = u"\u20B9"
            print(raw_text)

            context = {
                'estimate' : estimate,
                'product' : product,
                'raw_text' : raw_text,
                'sale' : sale,
                'gst' : gst,
                'product_gst' : product_gst,
                'word' : word
            }
            return render(request,"dashboard/saleinvoice.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

#Estimate sale Ajax Calls
@login_required(login_url='login')
def getproducts_estimate_sale(request):
    productdata = Product_estimate.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

@login_required(login_url='login')
def check_stock_estimate(request):
    pname = request.GET['pname']
    stock = Stock_estimate.objects.get(product=Product_estimate.objects.get(product_name=pname)).quantity

    return HttpResponse(stock)

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
    camount = customeraccount_estimate.objects.get(id = Customer_estimate.objects.get(fullname=cname).id)
    due_amount = camount.amount

    return HttpResponse(due_amount)

# GST sale Ajax Call
def getproducts_gst_sale(request):
    productdata = Product_gst.objects.all()
    return JsonResponse({"productdata":list(productdata.values())})

def customer_state_gst(request):
    cname = request.GET['cname'] 
    customer = Customer_gst.objects.get(id=Customer_gst.objects.get(fullname=cname).id)
    state = customer.state
    profile_state = request.user.profile.state

    return HttpResponse(state,profile_state)

def check_stock_gst(request):
    pname = request.GET['pname']
    stock = Stock_gst.objects.get(product=Product_gst.objects.get(product_name=pname)).quantity

    return HttpResponse(stock)

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
DailyIncomeData_estimate = 1
DailyIncomeData_gst = 1
@login_required(login_url='login')
def dailyincome(request):
    global DailyIncomeData_estimate
    global DailyIncomeData_gst
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
                DailyIncomeData_estimate = dailyincome_estimate.objects.filter(date=d2)

            if GST_group in user.groups.all():
                DailyIncomeData_gst = dailyincome_gst.objects.filter(date=d2)

            context = {
                'd1':d1,
                'DailyIncomeData_estimate':DailyIncomeData_estimate,
                'DailyIncomeData_gst':DailyIncomeData_gst,
            }
            return render(request, 'dashboard/dailyincome.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

estimate_category = 1
gst_category = 1
DailyExpenseData_estimate = 1
DailyExpenseData_gst = 1
@login_required(login_url='login')
def dailyexpense(request):
    global estimate_category
    global gst_category
    global DailyExpenseData_estimate
    global DailyExpenseData_gst
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
                DailyExpenseData_estimate = dailyexpense_estimate.objects.filter(date=d2)
                estimate_category = category_estimate.objects.all()

            if GST_group in user.groups.all():
                DailyExpenseData_gst = dailyexpense_gst.objects.filter(date=d2)
                gst_category = category_gst.objects.all()

            context = {
                'd1':d1,
                'DailyExpenseData_estimate':DailyExpenseData_estimate,
                'DailyExpenseData_gst':DailyExpenseData_gst,
                'estimate_category':estimate_category,
                'gst_category':gst_category
            }
            return render(request , 'dashboard/dailyexpense.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

supplierdata_estimate = 1
supplierdata_gst = 1
@login_required(login_url='login')
def supplierpayment(request):
    global supplierdata_estimate
    global supplierdata_gst
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:

                    SupplierPay = supplierpay_estimate(
                        supplier_name = supplieraccount_estimate.objects.get(id=request.POST['supplier-name']).supplier_name,
                        pending_amount = float(request.POST['pending_amount']),
                        paid_amount = float(request.POST['paid_amount'])
                    )
                
                    supplieraccountdata = supplieraccount_estimate.objects.get(id=request.POST['supplier-name'])

                    supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])

                    supplieraccountdata.save()
                    SupplierPay.save()
                    messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

                else:

                    SupplierPay = supplierpay_gst(
                        supplier_name = supplieraccount_gst.objects.get(id=request.POST['supplier-name']).supplier_name,
                        pending_amount = float(request.POST['pending_amount']),
                        paid_amount = float(request.POST['paid_amount'])
                    )
                
                    supplieraccountdata = supplieraccount_gst.objects.get(id=request.POST['supplier-name'])

                    supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])

                    supplieraccountdata.save()
                    SupplierPay.save()
                    messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

            if Estimate_group in user.groups.all():
                supplierdata_estimate = Supplier_estimate.objects.all()

            if GST_group in user.groups.all():
                supplierdata_gst = Supplier_gst.objects.all()

            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            context = {
                'd1':d1,
                'supplierdata_estimate' : supplierdata_estimate,
                'supplierdata_gst' : supplierdata_gst
            }
            return render(request, 'dashboard/supplierpayment.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

customerdata_estimate = 1
customerdata_gst = 1
@login_required(login_url='login')
def customerpayment(request):
    global customerdata_estimate
    global customerdata_gst
    Estimate_group = Group.objects.get(name="Estimate")
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:

                    CustomerPay = customerpay_estimate (
                        customer_name = customeraccount_estimate.objects.get(id=request.POST['customer']).customer_name,
                        pending_amount = request.POST['pending_amount'],
                        paid_amount = request.POST['paid_amount'],
                        Description = request.POST['Description']
                    )
                    CustomerPay.save()

                    customerdata = customeraccount_estimate.objects.get(id=request.POST['customer'])

                    customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])

                    customerdata.save()
                    messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")

                else:

                    CustomerPay = customerpay_gst (
                        customer_name = customeraccount_gst.objects.get(id=request.POST['customer']).customer_name,
                        pending_amount = request.POST['pending_amount'],
                        paid_amount = request.POST['paid_amount'],
                        Description = request.POST['Description']
                    )
                    CustomerPay.save()

                    customerdata = customeraccount_gst.objects.get(id=request.POST['customer'])

                    customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])

                    customerdata.save()
                    messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")
            

            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            if Estimate_group in user.groups.all():
                customerdata_estimate = customeraccount_estimate.objects.all()
            
            if GST_group in user.groups.all():
                customerdata_gst = customeraccount_gst.objects.all()

            context = {
                'd1':d1,
                'customerdata_estimate':customerdata_estimate,
                'customerdata_gst' : customerdata_gst
            }
            return render(request, 'dashboard/customerpayment.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def supplier_dueamount_estimate(request):
    sid = request.GET['sid']
    supplierdata = supplieraccount_estimate.objects.get(id = supplieraccount_estimate.objects.get(id=sid).id)
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
stock_data = 1
@login_required(login_url='login')
def list_stock(request):
    global stock_data
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    stockdata = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['product_name']))
                    stock_quantity = stockdata.quantity + int(request.POST['qty'])
                    stockdata.save()
                if 'GST' in request.POST:
                    stockdata = Stock_gst.objects.get(product = Product_gst.objects.get(product_name=request.POST['product_name']))
                    stock_quantity = stockdata.quantity + int(request.POST['qty'])
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
    if Estimate_group in user.groups.all():
        customer_payment = customerpay_estimate.objects.all()
    else:
        customer_payment = customerpay_gst.objects.all()

    context = {
        'customer_payment':customer_payment
    }
    return render(request, 'dashboard/customerpaymentlist.html',context)

@login_required(login_url='login')
def supplier_payment_list(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if Estimate_group in user.groups.all():
        supplier_payment = supplierpay_estimate.objects.all()
    else:
        supplier_payment = supplierpay_gst.objects.all()
    
    context = {
        'supplier_payment':supplier_payment
    }
    return render(request,"dashboard/supplierpaymentlist.html",context)

@login_required(login_url='login')
def customer_Credit(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if Estimate_group in user.groups.all():
        customer_credit_data = customeraccount_estimate.objects.all()
    else:
        customer_credit_data = customeraccount_gst.objects.all()
    
    context = {
        'customer_credit_data':customer_credit_data
    }
    return render(request, 'dashboard/customercredit.html',context)

@login_required(login_url='login')
def supplier_credit(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if Estimate_group in user.groups.all():
        supplier_credit_list = supplieraccount_estimate.objects.all()
    else:
        supplier_credit_list = supplieraccount_gst.objects.get()

    context = {
        'supplier_credit_list':supplier_credit_list
    }
    return render(request,'dashboard/suppliercredit.html',context)

@login_required(login_url='login')
def totalincome(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
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

@login_required(login_url='login')
def totalexpense(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
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

@login_required(login_url='login')
def salereport(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    if Estimate_group in user.groups.all():
        if request.method == 'POST':
            if 'Estimate' in request.POST:
                searchsale = Estimate_sales.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                context = {
                    'searchsale' : searchsale
                }
                return render(request,'dashboard/salereport.html',context)
        else:
            if request.method == 'POST':
                if 'GST' in request.POST:
                    searchsale = gstsale.objects.filter(date__gte = request.POST['fromdate'] , date__lte = request.POST['todate'])

                    context = {
                        'searchsale' : searchsale
                    }
                    return render(request,'dashboard/fromtowhere.html',context)

    total_estimate_sale = Estimate_sales.objects.all()
    total_gst_sale = gstsale.objects.all()
    
    context = {
        'total_estimate_sale' : total_estimate_sale,
        'total_gst_sale' : total_gst_sale,
    }
    return render(request,'dashboard/salereport.html',context)

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