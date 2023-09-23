from datetime import date
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Max
from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

from dashboard.models import *
from products.models import *
from payments.models import *
from Inventory.cache_storage import *

from .models import *


# To add / view and update sale data
@login_required(login_url='login')
def generate_bill_number(request):
    today = datetime.date.today()
    year = today.strftime("%Y")
    day_of_year = today.strftime("%j")

    # Assuming you have a model named Bill
    last_bill = Estimate_sale_bill_number.objects.all().first()

    if last_bill:
        last_bill_number = str(last_bill.last_bill_number)[8:]  # Extract the last part of the bill number
        new_bill_number = str(int(last_bill_number) + 1).zfill(3)  # Increment and pad with leading zeros
    else:
        new_bill_number = "001"  # First bill of the day
        bill_number = Estimate_sale_bill_number (
            last_bill_number = f"{year}{day_of_year}{new_bill_number}"
        )
        bill_number.save()

    return f"{year}{day_of_year}{new_bill_number}"

@login_required(login_url='login')
def addsale(request):
    if request.method == 'POST':
        # Check for User Group
        if request.session['Estimate']:
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
                Bill_no = request.POST['bill_no'],
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
            
            customer_data = customer_cache()
            
            if cash_on_hand != 0:
                # Create a object for Customer Pay when we have a Cash on Hand Value
                CustomerPay = customerpay_estimate (
                    customer_name = customer_data.get(id=request.POST['customer']),
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
            for i in range(0,int(request.POST['product_count'])):
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

            # Update the bill number in the Bill_number model.
            last_bill = Bill_number.objects.all().first()
            last_bill.last_bill_number = request.POST['bill_no']
            last_bill.save()
            
            # save
            customerAccount.save()
            Estimatesale.save()

        if request.session['GST']:
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
    if request.session['Estimate']:

        Product_data = product_cache()

        # Get the Product Data
        if request.session["Manufacture"]:
            Product_data = Product_data.filter(product_type = Product_type.objects.get(product_type="Manufacture"))
            
        
        # Get the customer Data
        customer_data = customer_cache()

        new_billno = generate_bill_number(request)
    
    if request.session['GST']:
        Product_data = Product_gst.objects.all()
        Customer_data = Customer_gst.objects.all()
        
        if gstsale.objects.all().exists():
            new_billno = gstsale.objects.last().Bill_no
            new_billno = new_billno + 1
        else:
            new_billno = 1

    context = {
        'Product_data' : Product_data,
        'Customer_data' : customer_data,
        'new_billno' : new_billno,
        'd1' : d1,
    }
    return render(request,"sales/sale.html",context)

@login_required(login_url='login')
def viewsale(request):
    # Check for user Group
    if request.session['Estimate']:
        # Get the sale data
        Sale_data = Estimate_sales.objects.all().prefetch_related("customer").order_by("-date")
    
    # Check for user Group
    if request.session['GST']:
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
        if request.session['Estimate']:
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
                customer = Customer_estimate.objects.get(id = request.POST['customer']),
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=request.POST['roff'],
                Grand_total=request.POST['gtot']
            )

            # Creating old amount
            old_amount = float(Grand_total) - float(old_grant_total) 

            # Get the customerAccount detail based on the customer
            customerAccount = customeraccount_estimate.objects.get(customer_name = request.POST['customer'])
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

        if request.session['GST']:

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
    if request.session['Estimate']:
        # To get the data to get display the update page
        sale_Bill_no = Estimate_sales.objects.get(pk=pk).Bill_no
        sale_data = Estimate_sales.objects.get(Bill_no=sale_Bill_no)
        sale_product = estimatesales_Product.objects.filter(Bill_no=sale_Bill_no)
        
        customer_data = customer_cache()

        product_data = product_cache()

        if request.user.groups.filter(name="Manufacture").exists():
            product_data = Product_estimate.objects.filter(product_type=Product_type.objects.get(product_type="Manufacture"))

    if request.session['GST']:
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
    
    template = get_template('sales/saleinvoice.html') 

    # Context data for rendering the template (replace with your actual data)
    context = {
        'logo': 'path/to/your/logo.png',
        'company_name': 'Company Name',
        'dated': '01/01/2000',
        'challan_number': '2023265002',
        'date': '01/01/2000',
        'cgst': 18,
        'sgst': 18,
        'cgst_amount': 2025.25,
        'sgst_amount': 2000.25,
        'total': 4025.50,
        'grand_total': 4025.50,
        'amount_in_words': 'Four Thousand and Twenty Five',
        'works': [  # Replace with your actual data
            {
                'code': 'Product Code',
                'vendor_name': 'Vendor Name',
                'po_number': 'PO123',
                'jc_number': 'JC456',
                'weight': '10 kg',
                'bags': 5,
                'quantity': 100,
                'rate': 20.50,
                'amount': 2050.00,
            },
            # Add more work items as needed
        ],
    }

    # Render the template with the context data
    html = template.render(context)

    # Create a PDF file
    pdf_file = HTML(string=html).write_pdf()

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'

    return response

# To get customer Due
''' We will get the Customer Due from the customerAccount model based on the customer name. 
This will hit on change of customer name. '''
@login_required(login_url='login')
def customerdue_estimate(request):
    cname = request.GET['cname']

    customer_data = customer_cache()

    customer_data = customer_data.get(id=cname)
    camount = customer_data.customeraccount_estimate
    due_amount = camount.amount

    return HttpResponse(due_amount)

# We will get the product details
''' Here we are checking for weather we have a product details in cache or not if we have then we will go with that or else create a cache here '''
@login_required(login_url='login')
def product_data_estimate(request):
    cache_key = "product_data_estimate_cache" 
    cached_productdata = cache.get(cache_key)

    productdata = product_cache()

    if request.session['Manufacture']:
        product_type = Product_type.objects.get(product_type = "Manufacture")
        productdata = productdata.filter(product_type = product_type)

    return JsonResponse({"productdata": list(productdata.values())})

# To get unit and stock quantity
''' This will hit on change of product. we will get the unit and quantity for that product, 
As we are validating that if the stock quantity for that product is 0 then we don't allow them to change the add the quantity to sell. ''' 
@login_required(login_url='login')
def selected_product(request):
    productname = request.GET['product_name']

    productdata = product_cache()
    
    product_data = productdata.get(product_name = productname)
    stock_data = Stock_estimate.objects.get(product = product_data.id)
    print(stock_data.quantity)

    if (stock_data.quantity == 0):
        quantity = 0
    else:
        quantity = stock_data.quantity

    product_data_values = {
        'product_name' : product_data.product_name,
        'product_unit' : product_data.unit,
        'quantity' : quantity,
        'rate' : product_data.selling_price
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