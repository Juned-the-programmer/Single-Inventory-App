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
from num2words import num2words

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

    if request.session["Estimate"]:
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

    if request.session["GST"]:
        # Assuming you have a model named Bill
        last_bill = GST_sale_bill_number.objects.all().first()

        if last_bill:
            last_bill_number = str(last_bill.last_bill_number)[8:]  # Extract the last part of the bill number
            new_bill_number = str(int(last_bill_number) + 1).zfill(3)  # Increment and pad with leading zeros
        else:
            new_bill_number = "001"  # First bill of the day
            bill_number = GST_sale_bill_number (
                last_bill_number = f"{year}{day_of_year}{new_bill_number}"
            )
            bill_number.save()

    return f"{year}{day_of_year}{new_bill_number}"

@login_required(login_url='login')
def addsale(request):
    if request.method == 'POST':
        # Check for User Group
        if request.session['Estimate']:
            # Load Customer Data
            customer_data = customer_cache()
            # Selected Customer
            selected_customer = customer_data.get(id=request.POST['customer'])

            # Load Product Data
            product_data = product_cache()

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
                customer = selected_customer,
                Total_amount=request.POST['total'],
                Due_amount=request.POST['oldamt'],
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )
            
            # Get the customerAccount data based on the customer name 
            customerAccount = selected_customer.customeraccount_estimate
            # Update the Grand Total
            customerAccount.amount = float(Grand_total)
            
            if cash_on_hand != 0:
                # Create a object for Customer Pay when we have a Cash on Hand Value
                CustomerPay = customerpay_estimate (
                    customer_name = selected_customer,
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

                # selected Product
                selected_product = product_data.get(product_name = request.POST['prod'+str(i)])

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
                stock = selected_product.stock_estimate
                stock.quantity = int(stock.quantity) - int(request.POST['qty'+str(i)])
                # save
                stock.save()
                # Save
                estimate.save()

            # Update the bill number in the Bill_number model.
            last_bill = Estimate_sale_bill_number.objects.all().first()
            last_bill.last_bill_number = request.POST['bill_no']
            last_bill.save()
            
            # save
            customerAccount.save()
            Estimatesale.save()

        if request.session['GST']:
            # Load Customer Data
            customer_data = customer_cache_gst()
            # selected customer data
            selected_customer = customer_data.get(id = request.POST['customer'])

            # Load Product data
            product_data = product_cache_gst()

            # Check for Round off values
            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
                print(Round_off)
            else:
                Round_off = 0
                print(Round_off )

            # Check for CGST
            if len(request.POST['cgst']) >= 1:
                CGST = request.POST['cgst']
            else:
                CGST = 0

            # Check for IGST
            if len(request.POST['igst']) >= 1:
                IGST = request.POST['igst']
            else:
                IGST = 0

            # Check for SGST
            if len(request.POST['sgst']) >= 1:
                SGST = request.POST['sgst']
            else:
                SGST = 0

            # Create a GST sale object
            GSTSALE = gstsale (
                Bill_no=request.POST['bill_no'],
                customer_name = selected_customer,
                total_amount=request.POST['total'],
                CGST=CGST,
                SGST=SGST,
                IGST=IGST,
                Round_off=Round_off,
                Grand_total=request.POST['gtot']
            )
            
            # Update the customer Account
            GSTCUSTOMER = selected_customer.customeraccount_gst
            grand_total = request.POST['gtot']
            GSTCUSTOMER.amount = float(GSTCUSTOMER.amount) + float(grand_total)
            
            # For Loop for Sale Products
            for i in range(0,int(request.POST['product_count'])):
                # Selected Product
                selected_product = product_data.get(product_name = request.POST['prod'+str(i)])

                # Creating product records
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

                # Updating stock details
                stock = selected_product.stock_gst
                stock.quantity = int(stock.quantity) - int(request.POST['qty'+str(i)])
                stock.save()

                # Save that product record.
                Gstsale.save()

            # Update the bill number in the Bill_number model.
            last_bill = GST_sale_bill_number.objects.all().first()
            last_bill.last_bill_number = request.POST['bill_no']
            last_bill.save()

            # Save Sale records and update the customer account.
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
        Product_data = product_cache_gst()

        # Get the Manufacture product Data 
        if request.session["Manufacture"]:
            Product_data = Product_data.filter(product_type = product_type_gst.objects.get(product_type="Manufacture"))

        # Get the Customer Data
        customer_data = customer_cache_gst()

        # Get New Bill Number
        new_billno = generate_bill_number(request)

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
        Sale_data = Estimate_sales.objects.all()
    
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
            for i in range(0,int(request.POST['product_count'])):
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
            # Load Customer Data
            customer_data = customer_cache_gst()
            selected_customer = customer_data.get(id=request.POST['customer'])
            customer_account = selected_customer.customeraccount_gst
            
            # Load Product Data
            productdata = product_cache_gst()

            # Get the Round Off Values
            if len(request.POST['roff']) >= 1:
                Round_off = request.POST['roff']
            else:
                Round_off = 0
                
            # Get the CGST Values
            if len(request.POST['cgst']) >= 1:
                CGST = request.POST['cgst']
            else:
                CGST = 0

            # Get the IGST Values
            if len(request.POST['igst']) >= 1:
                IGST = request.POST['igst']
            else:
                IGST = 0

            # Get the SGST Values
            if len(request.POST['sgst']) >= 1:
                SGST = request.POST['sgst']
            else:
                SGST = 0

            # Get the sales data
            sales_data = gstsale.objects.get(id = pk)
            Bill_no = sales_data.Bill_no
            sales_product = gstsales_Product.objects.filter(Bill_no = Bill_no)

            # Update Customer Acccount Values
            new_bill_total = float(request.POST['gtot']) - float(sales_data.Grand_total)
            customer_account.amount = customer_account.amount + new_bill_total
            customer_account.save()
            
            # Update Sale Record
            sales_data.customer_name = selected_customer
            sales_data.total_amount = request.POST['total']
            sales_data.CGST = CGST
            sales_data.IGST = IGST
            sales_data.SGST = SGST
            sales_data.Round_off = Round_off
            sales_data.Grand_total = request.POST['gtot']
            sales_data.save()

            # Update Stock data
            old_sales_product_count = int(sales_product.count())
            for i in range(0,int(old_sales_product_count)):
                product_data = productdata.get(product_name = sales_product[i].product_name)
                stock_data = product_data.stock_gst
                stock_data.quantity = int(stock_data.quantity) + int(sales_product[i].qty)
                stock_data.save()

            # Delete Existing Records for the Sales Product data
            sales_product.delete()

            # update Sales Product data
            new_sale_product_count = int(request.POST['product_count'])

            # Iterate through the products added.
            for i in range(0,int(new_sale_product_count)):
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

                # Load the product data
                product_data = productdata.get(product_name = request.POST['prod'+str(i)])
                # Update stock data
                stock = product_data.stock_gst
                stock.quantity = int(stock.quantity) - int(request.POST['qty'+str(i)])
                # Adding stock data
                stock.save()

                # Adding GST Sale product data
                Gstsale.save()

            return redirect('viewsale')


    # Check for user Grpup
    if request.session['Estimate']:
        # To get the data to get display the update page
        sale_Bill_no = Estimate_sales.objects.get(pk=pk).Bill_no
        sale_data = Estimate_sales.objects.get(Bill_no=sale_Bill_no)
        sale_product = estimatesales_Product.objects.filter(Bill_no=sale_Bill_no)
        
        customer_data = customer_cache()

        product_data = product_cache()

        if request.session["Manufacture"]:
            product_data = product_data.filter(product_type = Product_type.objects.get(product_type="Manufacture"))

    if request.session['GST']:
        # To get the data to get display the update page
        sale_Bill_no = gstsale.objects.get(pk=pk).Bill_no
        sale_data = gstsale.objects.get(Bill_no=sale_Bill_no)
        sale_product = gstsales_Product.objects.filter(Bill_no=sale_Bill_no)

        customer_data = customer_cache_gst()

        product_data = product_cache_gst()

        if request.session["Manufacture"]:
            product_data = product_data.filter(product_type = product_type_gst.objects.get(product_type="Manufacture"))


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

    # Get Bill details
    bill_detail = Estimate_sales.objects.get(id=pk)

    # Get product details
    product_detail = estimatesales_Product.objects.filter(Bill_no = bill_detail.Bill_no)

    # Company name
    company_name = request.user.profile.company_name

    # Mobile Number
    mobile_number = request.user.profile.phone_no

    # Address
    address = f"{request.user.profile.Address}, {request.user.profile.city}, {request.user.profile.state}, {request.user.profile.pincode}"

    # Amount in Words
    word_amount = str.upper(num2words(bill_detail.Grand_total))

    # Context data for rendering the template (replace with your actual data)
    context = {
        "bill_detail" : bill_detail,
        "product_detail" : product_detail,
        "company_name" : company_name,
        "mobile_number" : mobile_number,
        "address" : address,
        "word_amount" : word_amount
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
    if request.session["Estimate"]:
        productdata = product_cache()

        if request.session['Manufacture']:
            product_type = Product_type.objects.get(product_type = "Manufacture")
            productdata = productdata.filter(product_type = product_type)

    if request.session["GST"]:
        productdata = product_cache_gst()

        if request.session["Manufacture"]:
            product_type = product_type_gst.objects.get(product_type = "Manufacture")
            productdata = productdata.filter(product_type = product_type)

    return JsonResponse({"productdata": list(productdata.values())})

# To get unit and stock quantity
''' This will hit on change of product. we will get the unit and quantity for that product, 
As we are validating that if the stock quantity for that product is 0 then we don't allow them to change the add the quantity to sell. ''' 
@login_required(login_url='login')
def selected_product(request):
    if request.session["Estimate"]:
        productname = request.GET['product_name']

        productdata = product_cache()
        
        product_data = productdata.get(product_name = productname)
        stock_data = Stock_estimate.objects.get(product = product_data.id)
        print(stock_data.quantity)

        if (stock_data.quantity == 0):
            quantity = 0
        else:
            quantity = stock_data.quantity
    
    if request.session['GST']:
        productname = request.GET['product_name']

        productdata = product_cache_gst()

        product_data = productdata.get(product_name = productname)
        stock_data = product_data.stock_gst

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

# GST sale Ajax Call
def customer_state_gst(request):
    cname = request.GET['cname'] 
    customer_data = customer_cache_gst()
    customer = customer_data.get(id = cname)
    state = customer.state

    return HttpResponse(state)