from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from customer.models import *
from supplier.models import *

from .models import *


# Create your views here.
@login_required(login_url='login')
def supplierpayment(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
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

    if request.user.groups.filter(name='Estimate').exists():
        supplier_data = Supplier_estimate.objects.all()

    if request.user.groups.filter(name='GST').exists():
        supplier_data = Supplier_gst.objects.all()

    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")
    context = {
        'd1':d1,
        'supplier_data':supplier_data
    }
    return render(request, 'payments/supplierpayment.html',context)

@login_required(login_url='login')
def customerpayment(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
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
            customerdata = customeraccount_estimate.objects.get(id=request.POST['customer'])

            customerdata.amount  = float(request.POST['pending_amount']) - float(request.POST['paid_amount']) 
            customerdata.amount = customerdata.amount - float(round_off)

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
        customer_data = customeraccount_estimate.objects.all()
    
    if request.user.groups.filter(name='GST').exists():
        customer_data = customeraccount_gst.objects.all()

    context = {
        'd1':d1,
        'customer_data':customer_data
    }
    return render(request, 'payments/customerpayment.html',context)

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