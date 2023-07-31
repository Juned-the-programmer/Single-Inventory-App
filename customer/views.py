from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *


# Create your views here.
@login_required(login_url='login')
def addcustomer(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST:
                    customer = Customer_estimate(
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
                    customerdata_estimate = Customer_estimate.objects.all().count()
                    customer_id = customerdata_estimate + 1
                else:
                    customer_id = 1

            if GST_group in user.groups.all():
                if Customer_gst.objects.all().exists():
                    customerdata_gst = Customer_gst.objects.all().count()
                    customer_id = customerdata_gst + 1
                else:
                    customer_id = 1
            
            context = {
                'customer_id':customer_id
            }
            return render(request,"customer/addcustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')
    
@login_required(login_url='login')
def viewcustomer(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                customer_data = Customer_estimate.objects.all()
            
            if GST_group in user.groups.all():
                customer_data = Customer_gst.objects.all()

            context = {
                'customer_data':customer_data
            }
            return render(request,"customer/viewcustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')
    
@login_required(login_url='login')
def updatecustomer(request,pk):
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

            if Estimate_group in user.groups.all():
                customer_data = Customer_estimate.objects.get(pk=pk)


            if GST_group in user.groups.all():
                customer_data = Customer_gst.objects.get(pk=pk)

            context = {
                'customer_data':customer_data
            }
            return render(request,"customer/updatecustomer.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')