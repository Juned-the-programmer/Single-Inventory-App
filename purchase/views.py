from datetime import date
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Max
from django.core.cache import cache

from products.models import *
from Inventory.cache_storage import *

from .models import *

# To Add / view and update the purchase data
# To Add Purchase
@login_required(login_url='login')
def generate_bill_number(request):
    today = datetime.date.today()
    year = today.strftime("%Y")
    day_of_year = today.strftime("%j")

    if request.session['Estimate']:
        # Assuming you have a model named Bill
        last_bill = Estimate_purchase_bill_number.objects.all().first()

        if last_bill:
            last_bill_number = str(last_bill.last_bill_number)[8:]  # Extract the last part of the bill number
            new_bill_number = str(int(last_bill_number) + 1).zfill(3)  # Increment and pad with leading zeros
        else:
            new_bill_number = "001"  # First bill of the day
            bill_number = Estimate_purchase_bill_number (
                last_bill_number = f"{year}{day_of_year}{new_bill_number}"
            )
            bill_number.save()

        return f"{year}{day_of_year}{new_bill_number}"

    if request.session['GST']:
        # Assuming you have a model named Bill
        last_bill = Gst_purchase_bill_number.objects.all().first()

        if last_bill:
            last_bill_number = str(last_bill.last_bill_number)[8:]  # Extract the last part of the bill number
            new_bill_number = str(int(last_bill_number) + 1).zfill(3)  # Increment and pad with leading zeros
        else:
            new_bill_number = "001"  # First bill of the day
            bill_number = Estimate_purchase_bill_number_gst (
                last_bill_number = f"{year}{day_of_year}{new_bill_number}"
            )
            bill_number.save()

        return f"{year}{day_of_year}{new_bill_number}"

@login_required(login_url='login')
def addpurchase(request):
    
    # Load Estimate Product and Supplier data
    supplier_data = supplier_cache()
    product_data = product_cache()

    # Load GST Product and Supplier data
    supplier_data_gst = supplier_cache_gst()
    product_data_gst = product_cache_gst()

    if request.method == 'POST':
        # Check for User Group
        if request.session["Estimate"]:
            # Load Supplier Data 
            supplier_data = supplier_data.objects.get(id=request.POST['supplier'])

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
                supplier = supplier_data,
                Total_amount = request.POST['total'],
                Due_amount = Due_amount,
                Round_off = Round_off,
                Grand_total = request.POST['gtot']
            )
            
            # Get supplier account Estimate based on the supplier data
            supplierAccount = supplier_data.supplieraccount_estimate
            supplierAccount.amount = float(request.POST['gtot'])
            
            # Loop to save the data for product details for that sale.
            # estimate_purchase_product_list_count : See the declaration for more
            for i in range(0,int(request.POST['product_count'])):
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
                product_data = product_data.get(product_name=request.POST['prod'+str(i)])
                stock = product_data.stock_estimate
                quantity = stock.quantity
                quantity = int(quantity)
                stock.quantity = quantity + int(request.POST['qty'+str(i)])
                # Save
                stock.save()
                estimate.save()

                last_bill = Estimate_purchase_bill_number.objects.all().first()
                last_bill.last_bill_number = request.POST['bill_no']
                last_bill.save()

            # Save
            Estimate.save()
            supplierAccount.save()
            messages.success(request,"Purchase Added Successfully ! ")

        if request.session["GST"]:
            # Load Supplier data
            supplier_data = supplier_data_gst.get(id=request.POST['supplier_name'])

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
                supplier_name = supplier_data,
                total_amount=request.POST['total'],
                CGST=CGST,
                SGST=SGST,
                IGST=IGST,
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )

            if(request.FILES['purchase_invoice']):
                upload_file = request.FILES['purchase_invoice']
                if upload_file.name.endswith('.pdf'):
                    GSTPURCHASE.pdf_invoice = upload_file

            GSTSUPPLIER = supplier_data.supplieraccount_gst
            GSTSUPPLIER.amount = float(request.POST['gtot']) + float(GSTSUPPLIER.amount)
            
            for i in range(0,int(request.POST['product_count'])):
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

                product_data = product_data_gst.get(product_name = request.POST['prod'+str(i)])
                stock = product_data.stock_gst
                quantity = stock.quantity
                stock_there = int(quantity)
                stock_to_add = int(request.POST['qty'+str(i)])
                stock.quantity = stock_there + stock_to_add
                stock.save()
                Gstpurchase.save()

            last_bill = Gst_purchase_bill_number.objects.all().first()
            last_bill.last_bill_number = request.POST['bill_no']
            last_bill.save()

            GSTPURCHASE.save()
            GSTSUPPLIER.save()

            messages.success(request,"Purchase Added Successfully ! ")

    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")

    if request.session["Estimate"]:
        Supplier_data = supplier_cache()

        new_bill = generate_bill_number(request)

    if request.session["GST"]:
        Supplier_data = supplier_cache_gst()
        
        new_bill = generate_bill_number(request)

    context = {
        'Supplier_data' : Supplier_data,
        'new_bill' : new_bill,
        'd1' : d1,
    }
    return render(request,"purchase/purchase.html",context)

# To view Purchase data
@login_required(login_url='login')
def viewpurchase(request):
    # Check for user Group
    if request.session["Estimate"]:
        # Get the product data
        Purchase_data = Estimate_Purchase.objects.all().prefetch_related('supplier').order_by("-date")
    
    # Check for user Group
    if request.session["GST"]:
        # Get the product data
        Purchase_data = GST_Purchase.objects.prefetch_related('supplier_name').all().order_by("-date")

    context = {
        'Purchase_data' : Purchase_data
    }
    return render(request,"purchase/viewpurchase.html",context)

# To update the Purchase detail
@login_required(login_url='login')
def updatepurchase(request,pk):
    if request.method == 'POST':
        # Check for User group
        if request.session["Estimate"]:
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

        if request.session["GST"]:
            #Load the supplier Data
            supplier_data = supplier_cache_gst()
            supplierdata = supplier_data.get(id = request.POST['supplier'])
            supplier_account = supplierdata.supplieraccount_gst
            
            # Load Product Data
            productdata = product_cache_gst()

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
            
            # Get the purchase bill details
            purchase_data = GST_Purchase.objects.get(id = pk)
            Bill_no = purchase_data.Bill_no
            purchase_product = gstpurchase_Product.objects.filter(Bill_no = Bill_no)

            # Update the Supplier Account values
            new_bill_total = float(request.POST['gtot']) - float(purchase_data.Grand_total)
            supplier_account.amount = supplier_account.amount + new_bill_total
            supplier_account.save()

            # Update the Purchase Record
            purchase_data.supplier_name = supplierdata
            purchase_data.total_amount = request.POST['total']
            purchase_data.CGST = CGST
            purchase_data.SGST = SGST
            purchase_data.IGST = IGST
            purchase_data.Round_off = Round_off
            purchase_data.Grand_total = request.POST['gtot']
            purchase_data.save()

            # Update the Stock data
            old_purchase_product_count = int(purchase_product.count())
            for i in range(0,int(old_purchase_product_count)):
                product_data = productdata.get(product_name = purchase_product[i].product_name)
                stock_data = product_data.stock_gst
                stock_data.quantity = int(stock_data.quantity) - int(purchase_product[i].qty)
                stock_data.save()
            
            # Delete Existing Records for the Product Data
            purchase_product.delete()

            # Update Purchase Products
            new_purchase_product_count = int(request.POST['product_count'])

            for i in range(0,new_purchase_product_count):
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

                product_data = productdata.get(product_name = request.POST['prod'+str(i)])
                stock_data = product_data.stock_gst
                stock_data.quantity = int(stock_data.quantity) + int(request.POST['qty'+str(i)]) 
                stock_data.save()
                Gstpurchase.save()

            return redirect('viewpurchase')
            messages.success(request,"Purchase Successfully !")

    if request.user.groups.filter(name='Estimate').exists():
        purchase_Bill_no = Estimate_Purchase.objects.get(pk=pk).Bill_no
        purchase_Bill_date = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no).date
        purchase_data = Estimate_Purchase.objects.get(Bill_no=purchase_Bill_no)
        purchase_product = estimatepurchase_Product.objects.filter(Bill_no=purchase_Bill_no)
        
        supplier_data = supplier_cache()
        productdata = product_cache()
        
        if request.session["Manufacture"]:
            product_data = productdata.exclude(product_type=Product_type.objects.get(product_type="Manufacture"))
        else:
            product_data = productdata
    
    if request.user.groups.filter(name='GST').exists():
        purchase_Bill_no = GST_Purchase.objects.get(pk=pk).Bill_no
        purchase_Bill_date = GST_Purchase.objects.get(pk=pk).date
        purchase_data = GST_Purchase.objects.get(Bill_no=purchase_Bill_no)
        purchase_product = gstpurchase_Product.objects.filter(Bill_no=purchase_Bill_no)

        supplier_data = supplier_cache_gst()
        product_data = product_cache_gst()

        if request.session["Manufacture"]:
            product_data = product_data.exclude(product_type=product_type_gst.objects.get(product_type="Manufacture"))
        else:
            product_data = productdata
    
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
    if request.session["Estimate"]:
        # Purchase data based on ID
        Purchase_data = Estimate_Purchase.objects.get(pk=pk)
        # Purchase product data
        Purchase_data_product = estimatepurchase_Product.objects.filter(Bill_no = Purchase_data.Bill_no)
        word = 1
    
    # Check for user Group
    if request.session["GST"]:
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
    sname = request.GET['cname']

    supplier_data = supplier_cache()

    camount = supplier_data.get(id=sname).supplieraccount_estimate
    due_amount = camount.amount

    return HttpResponse(due_amount)

# To get the Purchase Price and unit for the selected product
@login_required(login_url='login')
def purchaseprice_estimate(request):
    if request.session['Estimate']:
        product_name = request.GET['pname']

        productdata = product_cache()

        prodct_data = productdata.get(product_name=product_name)
    
    if request.session['GST']:
        product_name = request.GET['pname']

        productdata = product_cache_gst()
        prodct_data = productdata.get(product_name=product_name)

    response_data = {
        "purchase_price" : prodct_data.purchase_price,
        "product_unit" : prodct_data.unit
    }
    return JsonResponse(response_data)

# To get the Products details based on the supplier selected
''' We will not get all the products at all for purchase we will filter out those products which we can purchase from this supplier.
It will reduce the complexity and increase data maintainability '''
@login_required(login_url='login')
def supplier_products(request):
    if request.session['Estimate']:
        productdata = product_cache()

        product_data = productdata.filter(supplier=request.GET['supplier_name']).exclude(product_type=Product_type.objects.get(product_type="Manufacture"))
        return JsonResponse({"Product_data":list(product_data.values())})

    if request.session['GST']:
        productdata = product_cache_gst()
        supplier_data = supplier_cache_gst()

        product_data = productdata.filter(supplier=request.GET['supplier_name']).exclude(product_type=product_type_gst.objects.get(product_type="Manufacture"))
        supplier_state = supplier_data.get(id=request.GET['supplier_name']).state
        return JsonResponse({"Product_data":list(product_data.values()) , "supplier_state" : supplier_state})