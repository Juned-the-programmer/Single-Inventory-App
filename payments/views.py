from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.cache import cache

from customer.models import *
from supplier.models import *

from .models import *

''' This is also a simple to add the customer and supplier payments to database and update the Accounts '''

# To add supplier Payments
@login_required(login_url='login')
def supplierpayment(request):
    if request.method == 'POST':
        # Check for User Group
        if request.user.groups.filter(name='Estimate').exists():
            # Check for round off value
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

            # Get the supplier Account details based on the supplier_name
            supplieraccountdata = supplieraccount_estimate.objects.get(supplier_name = request.POST['supplier-name'])

            # Update the amount for that Supplier Account accordingly
            supplieraccountdata.amount = float(request.POST['pending_amount']) - float(request.POST['paid_amount'])
            supplieraccountdata.amount = supplieraccountdata.amount - float(round_off)

            # Save
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

    # Check for user Group
    if request.user.groups.filter(name='Estimate').exists():
        # Get all the supplier data
        cache_key = "supplier_data_estimate_cache"
        cache_supplier_data = cache.get(cache_key)

        if cache_supplier_data is None:
            supplier_data = Supplier_estimate.objects.all()
            cache.set(cache_key, supplier_data , timeout=None)
        else:
            supplier_data = cache_supplier_data
    
    # Check for user Group
    if request.user.groups.filter(name='GST').exists():
        # Get all the supplier data
        supplier_data = Supplier_gst.objects.all()

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
        if request.user.groups.filter(name='Estimate').exists():
            # Check for round off value
            if len(request.POST['round_off']) >= 1:
                round_off = request.POST['round_off']
            else:
                round_off = 0

            CustomerPay = customerpay_estimate (
                customer_name = Customer_estimate.objects.get(id=request.POST['customer']),
                pending_amount = request.POST['pending_amount'],
                paid_amount = request.POST['paid_amount'],
                round_off = round_off,
                Description = request.POST['Description']
            )

            # Get the customerData based on the customer_name
            customerdata = customeraccount_estimate.objects.get(customer_name=request.POST['customer'])

            # Updating the amount value accordingly
            customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount']) 
            customerdata.amount = customerdata.amount - float(round_off)

            # Save
            CustomerPay.save()
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

    if request.user.groups.filter(name='Estimate').exists():
        cache_key = "customer_data_estimate_cache"
        cache_customer_data = cache.get(cache_key)

        if cache_customer_data is None:
            customer_data = Customer_estimate.objects.all()
            cache.set(cache_key, customer_data , timeout = None)
            print("Not Cached Data")
        else:
            customer_data = cache_customer_data
            print("Cached Data")
    
    if request.user.groups.filter(name='GST').exists():
        customer_data = Customer_gst.objects.all()

    context = {
        'd1':d1,
        'customer_data':customer_data
    }
    return render(request, 'payments/customerpayment.html',context)

# To get the supplier due amount for Estimate
@login_required(login_url='login')
def supplier_dueamount_estimate(request):
    sid = request.GET['sid']

    cache_key = "supplier_data_estimate_cache"
    cache_supplier_data = cache.get(cache_key)

    if cache_supplier_data is None:
        supplier_data = Supplier_estimate.objects.all()
        cache.set(cache_key, supplier_data , timeout=None)
        print("Not Cached Data")
    else:
        supplier_data = cache_supplier_data
        print("cached Data")

    supplierdata = supplier_data.get(id=sid)
    supplier_account = supplierdata.supplieraccount_estimate
    pendingamount = supplier_account.amount

    return HttpResponse(pendingamount)

# To get the customer due amount for Estimate
@login_required(login_url='login')
def customer_dueamount_estimate(request):
    cid = request.GET['cid']

    cache_key = "customer_data_estimate_cache"
    cache_customer_data = cache.get(cache_key)

    if cache_customer_data is None:
        customer_data = Customer_estimate.objects.all()
        cache.set(cache_key, customer_data , timeout = None)
        print("Not Cached Data")
    else:
        customer_data = cache_customer_data
        print("Cached Data")

    customerdata = customer_data.get(id=cid)
    customer_account = customerdata.customeraccount_estimate
    pendingamount = customer_account.amount

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