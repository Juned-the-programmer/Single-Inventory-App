from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Max
from django.core.cache import cache

from dashboard.models import *
from products.models import *

from .models import *


# To add / view and update sale data
@login_required(login_url='login')
def addsale(request):
    if request.method == 'POST':
        # Check for User Group
        if request.user.groups.filter(name='Estimate').exists():
            # Check for cash on Hand Value
            if len(request.POST['cod']):
                cash_on_hand = request.POST['cod']
            else:
                cash_on_hand = 0
            
            # Check for Round off value
            if len(request.POST['roff']):
                Round_off = request.POST['roff']
            else:
                Round_off = 0

            Grand_total = request.POST['gtot']
        
            # Create a Estimate sale data
            Estimatesale = Estimate_sales(
                Bill_no=request.POST['bill_no'],
                customer = Customer_estimate.objects.get(id=request.POST['customer']),
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )
            
            # Get the customerAccount data based on the customer name 
            customerAccount = customeraccount_estimate.objects.get(customer_name = request.POST['customer'])
            # Update the Grand Total
            customerAccount.amount = float(Grand_total)
            
            if cash_on_hand == 0:
                print("Customer Payment")
            else:
                # Create a object for Customer Pay when we have a Cash on Hand Value
                CustomerPay = customerpay_estimate (
                    customer_name = request.POST['customer'],
                    pending_amount = Grand_total,
                    paid_amount = cash_on_hand,
                    round_off = 0
                )
                # Save
                CustomerPay.save()
                # update customer Account 
                customerAccount.amount  = float(customerAccount.amount) - float(cash_on_hand)

            # Loop through the list of prodcuts for that Sale
            # esc : Check for declaration
            for i in range(0,esc):
                if len(request.POST['dis'+str(i)]) >= 1:
                    dis = request.POST['dis'+str(i)]
                else:
                    dis = 0

                # Create a object
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

                # Get the stock details based on the product_name
                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                # Update the quantity
                b = int(request.POST['qty'+str(i)])
                stock.quantity = a - b
                # save
                stock.save()
                # Save
                estimate.save()
            
            # save
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

    # Check for user Group
    if request.user.groups.filter(name='Estimate').exists():
        # Get the Product Data
        Product_data = Product_estimate.objects.all()
        # Get the customer Data
        Customer_data = Customer_estimate.objects.all()

        # To get the Bill no
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
    # Check for user Group
    if request.user.groups.filter(name='Estimate').exists():
        # Get the sale data
        Sale_data = Estimate_sales.objects.all()
    
    # Check for user Group
    if request.user.groups.filter(name='GST').exists():
        # Get the sale data
        Sale_data = gstsale.objects.all()

    context = {
        'Sale_data' : Sale_data
    }
    return render(request,"sales/viewsale.html",context)

# Update the sale data
@login_required(login_url='login')
def updatesale(request , pk):
    if request.method == 'POST':
        # Check for user Group
        if request.user.groups.filter(name='Estimate').exists():
            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
            else:
                Round_off = 0

            Grand_total = request.POST['gtot']
            old_grant_total =  request.POST['cod']

            # Get the product count for that bill no
            saleproduct_count = estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no']).count()
            # Get the bill products
            bill_product = estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no'])
            
            # Iterate the loop to get update the stock data
            for j in range(0,saleproduct_count):
                print(bill_product[j].product_name)
                # Get the stock data
                add_stock = Stock_estimate.objects.get(product=Product_estimate.objects.get(product_name=bill_product[j].product_name))
                # Update the stock quantity accordingly
                add_stock.quantity = add_stock.quantity + bill_product[j].qty
                # save
                add_stock.save()

            # Delete the sale data
            Estimate_sales.objects.get(Bill_no=request.POST['bill_no']).delete()
            estimatesales_Product.objects.filter(Bill_no=request.POST['bill_no']).delete()

            # Create a new object for sale
            Estimatesale = Estimate_sales(
                Bill_no=request.POST['bill_no'],
                customer = Customer_estimate.objects.get(id = Customer_estimate.objects.get(fullname=request.POST['customer']).id),
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=request.POST['roff'],
                Grand_total=request.POST['gtot']
            )

            # Creating old amount
            old_amount = float(Grand_total) - float(old_grant_total) 

            # Get the customerAccount detail based on the customer
            customerAccount = customeraccount_estimate.objects.get(customer_name = Customer_estimate.objects.get(fullname=request.POST['customer']))
            # Update the customer Account
            customerAccount.amount = float(customerAccount.amount) + float(old_amount) 
            
            # Irerate loop to get add the products for that sale
            for i in range(0,esc):
                if len(request.POST['dis'+str(i)]) >= 1:
                    dis = request.POST['dis'+str(i)]
                else:
                    dis = 0
                
                # Creating a Object
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
                
                # Get the stock data based on the product_name
                stock = Stock_estimate.objects.get(product = Product_estimate.objects.get(product_name=request.POST['prod'+str(i)]))
                c = stock.quantity
                a = int(c)
                b = int(request.POST['qty'+str(i)])
                # Update stock quantity
                stock.quantity = a - b
                # Save
                stock.save()
                estimate.save()

            # Save
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


    # Check for user Grpup
    if request.user.groups.filter(name='Estimate').exists():
        # To get the data to get display the update page
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

# To generate the Sale Invoice
@login_required(login_url='login')
def saleinvoice(request,pk):
    try:
        # Check for User group
        if request.user.groups.filter(name='Estimate').exists():
            # Get the sale data
            sale_data = Estimate_sales.objects.get(pk=pk)
            # Get the Product data
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

# To get the selling price for that product.
''' We will get selling price for that product. We will get that customer last bill number and check for at what price we have sold the item.
If we don't have then we will go with the regular price. 
This will hit on change of product name'''
@login_required(login_url='login')
def sellingprice_estimate(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    
    # Get the latest Bill_no for the customer
    last_bill_no = Estimate_sales.objects.filter(customer=cname).aggregate(Max('Bill_no'))['Bill_no__max']
    
    if last_bill_no:
        # Get the latest product rate for the customer and product
        last_rate = estimatesales_Product.objects.filter(Bill_no=last_bill_no, product_name=pname).last()
        if last_rate:
            return HttpResponse(last_rate.rate)
    
    # If no relevant records found, fallback to product estimate
    last_price = Product_estimate.objects.get(product_name=pname).selling_price
    return HttpResponse(last_price)

# To get the discount for that product.
''' Same like selling price for this also we will get the last bill number and check for what is the discount for that customer.
And if it is not then we will go with 0 
This will hit on change of product name'''
@login_required(login_url='login')
def previous_discount_estimate(request):
    pname = request.GET['pname']
    cname = request.GET['cname']
    
    # Get the latest Bill_no for the customer
    last_bill_no = Estimate_sales.objects.filter(customer=cname).aggregate(Max('Bill_no'))['Bill_no__max']
    
    if last_bill_no:
        # Get the latest product discount for the customer and product
        last_discount = estimatesales_Product.objects.filter(Bill_no=last_bill_no, product_name=pname).last()
        if last_discount:
            return HttpResponse(last_discount.dis)
    
    # If no relevant records found, return 0.0 as default
    return HttpResponse(0.0)

# To get customer Due
''' We will get the Customer Due from the customerAccount model based on the customer name. 
This will hit on change of customer name. '''
@login_required(login_url='login')
def customerdue_estimate(request):
    cname = request.GET['cname']
    camount = customeraccount_estimate.objects.get(customer_name = cname)
    due_amount = camount.amount

    return HttpResponse(due_amount)

# We will get the product details
''' Here we are checking for weather we have a product details in cache or not if we have then we will go with that or else create a cache here '''
@login_required(login_url='login')
def product_data_estimate(request):
    cache_key = "product_data_estimate_cache" 
    cached_productdata = cache.get(cache_key)

    # Check for caching data weather that is there or not.
    if cached_productdata is None:
        productdata = list(Product_estimate.objects.values())
        cache.set(cache_key, productdata, timeout=None)
        print("Non Cached Data")
    else:
        productdata = cached_productdata
        print("cached Data")

    return JsonResponse({"productdata": productdata})

# To get unit and stock quantity
''' This will hit on change of product. we will get the unit and quantity for that product, 
As we are validating that if the stock quantity for that product is 0 then we don't allow them to change the add the quantity to sell. ''' 
@login_required(login_url='login')
def selected_product(request):
    productname = request.GET['product_name']
    product_data = Product_estimate.objects.get(product_name= productname)
    stock_data = Stock_estimate.objects.get(product = product_data.id)
    print(stock_data.quantity)

    if (stock_data.quantity == 0):
        quantity = 0
    else:
        quantity = stock_data.quantity

    product_data_values = {
        'product_name' : product_data.product_name,
        'product_unit' : product_data.unit,
        'quantity' : quantity
    }

    return JsonResponse({"product_data" : product_data_values})

# To get the count for the products what we have added in the sales.
''' It will get the count of that how many products are there in that sale record what we are adding '''
def estimatesalec(request):
    global esc
    esc=int(request.GET['c'])
    return HttpResponse(esc)

# GST sale Ajax Call
def gstsalec(request):
    global gst
    gst=int(request.GET['c'])
    return HttpResponse(gst)

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