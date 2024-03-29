from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.cache import cache

from customer.models import *
from supplier.models import *
from Inventory.cache_storage import *

from .models import *

''' This is also a simple to add the customer and supplier payments to database and update the Accounts '''

# To add supplier Payments
@login_required(login_url='login')
def supplierpayment(request):
    if request.method == 'POST':
        # Check for User Group
        if request.session['Estimate']:
            # Check for round off value
            if len(request.POST['round_off']) >= 1:
                round_off = request.POST['round_off']
            else:
                round_off = 0

            # Get all the supplier data
            supplier_data = supplier_cache()

            SupplierPay = supplierpay_estimate(
                supplier_name = supplier_data.get(id=request.POST['supplier-name']),
                pending_amount = float(request.POST['pending_amount']),
                paid_amount = float(request.POST['paid_amount']),
                round_off = round_off
            )

            # Get the supplier Account details based on the supplier_name
            supplieraccountdata = supplier_data.get(id=request.POST['supplier-name']).supplieraccount_estimate

            # Update the amount for that Supplier Account accordingly
            supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
            supplieraccountdata.amount = supplieraccountdata.amount - float(round_off)

            # Save
            supplieraccountdata.save()
            SupplierPay.save()
            messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

        else:
            #  Check for round off value
            if len(request.POST['round_off']) >= 1:
                round_off = request.POST['round_off']
            else:
                round_off = 0

            # Get all the supplier data
            SupplierPay = supplierpay_gst(
                supplier_name = supplieraccount_gst.objects.get(id=request.POST['supplier-name']).supplier_name,
                pending_amount = float(request.POST['pending_amount']),
                paid_amount = float(request.POST['paid_amount']),
                round_off = round_off
            )

            # Get the supplier Account details based on the supplier_name
            supplieraccountdata = supplieraccount_gst.objects.get(id=request.POST['supplier-name'])

            # Update the amount for that supplier accordingly
            supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
            supplieraccountdata.amount = supplieraccountdata.amount - float(round_off)

            # save
            supplieraccountdata.save()
            SupplierPay.save()
            messages.success(request,"Supplier Payment Done Successfully of "+request.POST['paid_amount']+"!")

    # Check for user Group
    if request.session['Estimate']:
        # Get all the supplier data
        supplier_data = supplier_cache()
    
    # Check for user Group
    if request.session['GST']:
        # Get all the supplier data
        supplier_data = supplier_cache_gst()

    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")
    context = {
        'd1':d1,
        'supplier_data':supplier_data
    }
    return render(request, 'payments/supplierpayment.html',context)

# To add customer payment
@login_required(login_url='login')
def customerpayment(request):
    if request.method == 'POST':
        # Check for User Group
        if request.session['Estimate']:
            # Check for round off value
            if len(request.POST['round_off']) >= 1:
                round_off = request.POST['round_off']
            else:
                round_off = 0

            customer_data = customer_cache()

            CustomerPay = customerpay_estimate (
                customer_name = customer_data.get(id=request.POST['customer']),
                pending_amount = request.POST['pending_amount'],
                paid_amount = request.POST['paid_amount'],
                round_off = round_off,
                Description = request.POST['Description']
            )

            # Get the customerData based on the customer_name
            customerdata = customer_data.get(id=request.POST['customer']).customeraccount_estimate

            # Updating the amount value accordingly
            customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount']) 
            customerdata.amount = customerdata.amount - float(round_off)

            # Save
            CustomerPay.save()
            customerdata.save()
            messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")

        else:
            # Check for round off values
            if len(request.POST['round_off']) >= 1:
                round_off = request.POST['round_off']
            else:
                round_off = 0

            # Load customer data
            customer_data = customer_cache_gst()

            CustomerPay = customerpay_gst (
                customer_name = customer_data.get(id=request.POST['customer']),
                pending_amount = request.POST['pending_amount'],
                paid_amount = request.POST['paid_amount'],
                round_off = round_off,
                Description = request.POST['Description']
            )

            # Load the customer account data
            customerdata = customer_data.get(id=request.POST['customer']).customeraccount_gst

            # Update the customer account 
            customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
            customerdata.amount = customerdata.amount - float(round_off)

            # Save
            customerdata.save()
            CustomerPay.save()
            messages.success(request,"Payment Done Successfully of "+request.POST['paid_amount']+"!")
    

    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")

    if request.session['Estimate']:
        
        customer_data = customer_cache()
    
    if request.session['GST']:
        customer_data = customer_cache_gst()
    
    context = {
        'd1':d1,
        'customer_data':customer_data
    }
    return render(request, 'payments/customerpayment.html',context)

# To get the supplier due amount for Estimate
@login_required(login_url='login')
def supplier_dueamount(request):
    if request.session["Estimate"]:
        supplier_name = request.GET['supplier_name']

        supplier_data = supplier_cache()

        supplierdata = supplier_data.get(id = supplier_name)
        supplier_account = supplierdata.supplieraccount_estimate
        pendingamount = supplier_account.amount
    
    if request.session["GST"]:
        supplier_name = request.GET['supplier_name']

        supplier_data = supplier_cache_gst()

        supplierdata = supplier_data.get(id = supplier_name)
        supplier_account = supplierdata.supplieraccount_gst
        pendingamount = supplier_account.amount

    return HttpResponse(pendingamount)

# To get the customer due amount for Estimate
@login_required(login_url='login')
def customer_dueamount(request):
    if request.session["Estimate"]:
        customer_name = request.GET['customer_name']

        customer_data = customer_cache()

        customerdata = customer_data.get(id=customer_name)
        customer_account = customerdata.customeraccount_estimate
        pendingamount = customer_account.amount

    if request.session["GST"]:
        customer_name = request.GET['customer_name']

        customer_data = customer_cache_gst()

        customerdata = customer_data.get(id = customer_name)
        customer_account = customerdata.customeraccount_gst
        pendingamount = customer_account.amount

    return HttpResponse(pendingamount)