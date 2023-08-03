import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render

from .models import *

# Create your views here.

def is_unique_id_unique(unique_id, request):
    #Check for the Unique ID
    if request.user.groups.filter(name='Estimate').exists():
        from .models import Customer_estimate
        return not Customer_estimate.objects.filter(customer_id=unique_id).exists()
    
    if request.user.groups.filter(name='GST').exists():
        from .models import Customer_gst
        return not Customer_gst.objects.filter(customerid=unique_id).exists()

def generate_unique_id(full_name, request):
    # Extract first letter of first name and last name from the full name
    length=6
    first_name, _, last_name = full_name.partition(" ")
    first_name = first_name[:1]
    last_name = last_name[:1]

    # Generate a random string of digits
    random_digits = ''.join(random.choices(string.digits, k=length - 2))

    # Combine the first letter of the first name and the first letter of the last name with the random digits
    unique_id = (first_name + last_name + random_digits).upper()

    while not is_unique_id_unique(unique_id, request):
        # If the generated unique_id is not unique, generate a new one
        random_digits = ''.join(random.choices(string.digits, k=length - 2))
        unique_id = (first_name + last_name + random_digits).upper()

    return unique_id

@login_required(login_url='login')
def addsupplier(request):
    try:
        if request.method == 'POST':
            if request.user.groups.filter(name='Estimate').exists():
                supplier = Supplier_estimate(
                    supplier_id=generate_unique_id(request.POST['fullname'], request),
                    fullname = request.POST['fullname'],
                    contactno = request.POST['mobile'],
                    city = request.POST['city'],
                    state = request.POST['state'],
                    landmark = request.POST['landmark']
                )
                supplier.save()
                messages.success(request , "Added Supplier Successfully ! ")
           
            if request.user.groups.filter(name='GST').exists():
                supplier = Supplier_gst(
                    supplierid=generate_unique_id(request.POST['fullname'], request),
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
                
        if request.user.groups.filter(name='Estimate').exists():
            if Supplier_estimate.objects.all().exists():
                supplierdata_estimate = Supplier_estimate.objects.all().count()
                supplierid_estimate = supplierdata_estimate + 1
            else:
                supplierid_estimate = 1

        if request.user.groups.filter(name='GST').exists():
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
    except:
        return redirect('error404')


@login_required(login_url='login')
def viewsupplier(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            supplier_data = Supplier_estimate.objects.all()
            
        if request.user.groups.filter(name='GST').exists():
            supplier_data = Supplier_gst.objects.all()

        context = {
            'supplier_data': supplier_data
        }
        return render(request,"supplier/viewsupplier.html",context)
    except:
        return redirect('error404')


@login_required(login_url='login')
def updatesupplier(request,pk):
    try:
        if request.method == 'POST':
            if request.user.groups.filter(name='Estimate').exists():
                supplier = Supplier_estimate.objects.get(pk=pk)

                supplier.fullname = request.POST['fullname']
                supplier.customerid = request.POST['customerid']
                supplier.contactno = request.POST['mobile']
                supplier.city = request.POST['city']
                supplier.state = request.POST['state']
                supplier.landmark = request.POST['landmark']

                supplier.save()
                messages.success(request,"Update Supplier Successfully ! ")
            
            if request.user.groups.filter(name='GST').exists():
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

        if request.user.groups.filter(name='Estimate').exists():
            supplier_data = Supplier_estimate.objects.get(pk=pk)

        if request.user.groups.filter(name='GST').exists():
            supplier_data = Supplier_gst.objects.get(pk=pk)
            
        context = {
            'supplier_data':supplier_data
        }
        return render(request,"supplier/updatesupplier.html",context)
    except:
        return redirect('error404')