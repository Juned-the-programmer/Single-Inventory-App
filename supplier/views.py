from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render

from .models import *


# Create your views here.
@login_required(login_url='login')
def addsupplier(request):
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    supplier = Supplier_estimate(
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
                supplierdata_estimate = Supplier_estimate.objects.all().count()
                supplierid_estimate = supplierdata_estimate + 1
            else:
                supplierid_estimate = 1

            if Supplier_gst.objects.all().exists():
                supplierdata_gst = Supplier_gst.objects.all().count()
                supplierid_gst = supplierdata_gst + 1
            else:
                supplierid_gst = 1
            
            context = {
                'supplierid_estimate' : supplierid_estimate,
                'supplierid_gst' : supplierid_gst
            }
            return render(request,"supplier/addsupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')


@login_required(login_url='login')
def viewsupplier(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                supplier_data = Supplier_estimate.objects.all()
            if GST_group in user.groups.all():
                supplier_data = Supplier_gst.objects.all()

            context = {
                'supplier_data': supplier_data
            }
            return render(request,"supplier/viewsupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')


@login_required(login_url='login')
def updatesupplier(request,pk):
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

            if Estimate_group in user.groups.all():
                supplier_data = Supplier_estimate.objects.get(pk=pk)

            if GST_group in user.groups.all():
                supplier_data = Supplier_gst.objects.get(pk=pk)
            context = {
                'supplier_data':supplier_data
            }
            return render(request,"supplier/updatesupplier.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')