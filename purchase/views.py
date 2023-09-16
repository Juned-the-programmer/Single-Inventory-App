from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Max

from products.models import *

from .models import *

# To Add / view and update the purchase data

# To Add Purchase
@login_required(login_url='login')
def addpurchase(request):
    if request.method == 'POST':
        # Check for User Group
        if request.user.groups.filter(name='Estimate').exists():
            # Check for round off values
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
                supplier = Supplier_estimate.objects.get(id=request.POST['supplier']),
                Total_amount = request.POST['total'],
                Due_amount = Due_amount,
                Round_off = Round_off,
                Grand_total = request.POST['gtot']
            )
            
            # Get supplier account Estimate based on the supplier data
            supplierAccount = supplieraccount_estimate.objects.get(supplier_name = request.POST['supplier'])
            supplierAccount.amount = float(request.POST['gtot'])
            
            # Loop to save the data for product details for that sale.
            # estimate_purchase_product_list_count : See the declaration for more
            for i in range(0,estimate_purchase_product_list_count):
                # Check for discount
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

                # Update stock for that Product
                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                stock.quantity = a + int(request.POST['qty'+str(i)])
                # Save
                stock.save()
                estimate.save()

            # Save
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
        Supplier_data = Supplier_estimate.objects.all()

        if Estimate_Purchase.objects.exists():
            new_bill = Estimate_Purchase.objects.all().count()
            new_bill = new_bill + 1
        else:
            new_bill = 1

    if request.user.groups.filter(name='GST').exists():
        Supplier_data = Supplier_gst.objects.all()

        if GST_Purchase.objects.exists():
            new_bill = GST_Purchase.objects.last().Bill_no
            new_bill = new_bill + 1
        else:
            new_bill = 1

    context = {
        'Supplier_data' : Supplier_data,
        'new_bill' : new_bill,
        'd1' : d1,
    }
    return render(request,"purchase/purchase.html",context)

# To view Purchase data
@login_required(login_url='login')
def viewpurchase(request):
    try:
        # Check for user Group
        if request.user.groups.filter(name='Estimate').exists():
            # Get the product data
            Purchase_data = Estimate_Purchase.objects.all()
        
        # Check for user Group
        if request.user.groups.filter(name='GST').exists():
            # Get the product data
            Purchase_data = GST_Purchase.objects.all()

        context = {
            'Purchase_data' : Purchase_data
        }
        return render(request,"purchase/viewpurchase.html",context)
    except:
        return redirect('error404')

# To update the Purchase detail
@login_required(login_url='login')
def updatepurchase(request,pk):
    if request.method == 'POST':
        # Check for User group
        if request.user.groups.filter(name='Estimate').exists():
            # Update Round off
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

            # Get the count for the purchase products
            purchase_product_count = estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
            # Get the product details for that purchase made
            bill_product = estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no'])

            # Iterate loop through the Stock model to update and minus the quantity what we have purchased it.
            for j in range(0,purchase_product_count):
                print(bill_product[j].product_name)
                # Get the stock detail based on that product_name
                add_stock = Stock_estimate.objects.get(product=Product_estimate.objects.get(product_name=bill_product[j].product_name))
                # Minus the quantity from the stock for now
                add_stock.quantity = add_stock.quantity - bill_product[j].qty
                # Update the stock model
                add_stock.save()

            # Deleting the Estimate Purchase and purchase product data both.
            Estimate_Purchase.objects.get(Bill_no=request.POST['bill_no']).delete()
            estimatepurchase_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

            # Creating a object to save it.
            Estimate = Estimate_Purchase(
                Bill_no = request.POST['bill_no'],
                supplier = Supplier_estimate.objects.get(id = request.POST['supplier']),
                Total_amount = request.POST['total'],
                Due_amount = Due_amount,
                Round_off = Round_off,
                Grand_total = request.POST['gtot']
            )
            
            # Get the old amount
            old_amount = float(request.POST['gtot']) - float(old_grant_total) 

            # Get the supplier account based on the supplier data
            supplierAccount = supplieraccount_estimate.objects.get(supplier_name =request.POST['supplier'])
            # updating amount
            supplierAccount.amount = float(supplierAccount.amount) + float(old_amount)
            
            # Iterate loop to add the records
            for i in range(0,estimate_purchase_product_list_count):
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

                # Get the stock details based on the product name
                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                # Updating the stock details
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
        product_data = Product_estimate.objects.exclude(product_type=Product_type.objects.get(product_type="Manufacture"))
    
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

# Get the required data to generate the Invoice.
@login_required(login_url='login')
def purchaseinvoice(request,pk):
    # Check for user Group
    if request.user.groups.filter(name='Estimate').exists():
        # Purchase data based on ID
        Purchase_data = Estimate_Purchase.objects.get(pk=pk)
        # Purchase product data
        Purchase_data_product = estimatepurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
        word = 1
    
    # Check for user Group
    if request.user.groups.filter(name='GST').exists():
        # Purchase data based on ID
        Purchase_data = GST_Purchase.objects.get(pk=pk)
        # Purchase product data
        Purchase_data_product = gstpurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
        word = num2words(gst.Grand_total)

    raw_text = u"\u20B9"
    print(raw_text)

    context = {
        'Purchase_data' : Purchase_data,
        'Purchase_data_product' : Purchase_data_product,
        'word' : word
    }
    return render(request,"purchase/purchaseinvoice.html",context)

# To get the supplier due amount.
''' We will hit this on change event of Supplier name, When we will select the Supplier name it will get the due amount for that Supplier. '''
@login_required(login_url='login')
def supplierdueamount_estimate(request):
    cname = request.GET['cname']
    camount = supplieraccount_estimate.objects.get(supplier_name = cname)
    due_amount = camount.amount

    return HttpResponse(due_amount)

# To get the Purchase Price and unit for the selected product
@login_required(login_url='login')
def purchaseprice_estimate(request):
    product_name = request.GET['pname']
    supplier_name = request.GET['sname']
    
    # Get the Product details
    prodct_data = Product_estimate.objects.get(product_name=product_name)

    response_data = {
        "purchase_price" : prodct_data.purchase_price,
        "product_unit" : prodct_data.unit
    }
    return JsonResponse(response_data)

# To get count for the list of product for that purchase record.
''' This method will give us the count for how many product does it have in the purchase bill 
So we can use that to iterate the loop to save the product details for that purchase '''
@login_required(login_url='login')
def estimate_purchase_count(request):
    global estimate_purchase_product_list_count
    estimate_purchase_product_list_count=int(request.GET['estimate_purchase_product_count'])
    return HttpResponse(estimate_purchase_product_list_count)

# To get the Products details based on the supplier selected
''' We will not get all the products at all for purchase we will filter out those products which we can purchase from this supplier.
It will reduce the complexity and increase data maintainability '''
@login_required(login_url='login')
def supplier_products(request):
    product_data = Product_estimate.objects.filter(supplier=request.GET['supplier_name']).exclude(product_type=Product_type.objects.get(product_type="Manufacture"))
    return JsonResponse({"Product_data":list(product_data.values())})

# GST Start Here
@login_required(login_url='login')
def gstpurchasec(request):
    global gstp
    gstp=int(request.GET['c'])
    return HttpResponse(gstp)

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