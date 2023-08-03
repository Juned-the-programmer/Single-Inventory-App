import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

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
def addcustomer(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
            customer = Customer_estimate(
                customer_id=generate_unique_id(request.POST['fullname'], request),
                fullname = request.POST['fullname'],
                contactno = request.POST['mobile'],
                city = request.POST['city'],
                state = request.POST['state'],
                landmark = request.POST['landmark']
            )
            customer.save()
            messages.success(request , "Added Customer Successfully ! ")
        
        if request.user.groups.filter(name='GST').exists():
            customer = Customer_gst(
                customerid=generate_unique_id(request.POST['fullname'], request),
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

    if request.user.groups.filter(name='Estimate').exists():
        if Customer_estimate.objects.all().exists():
            customerdata_estimate = Customer_estimate.objects.all().count()
            customer_id = customerdata_estimate + 1
        else:
            customer_id = 1

    if request.user.groups.filter(name='GST').exists():
        if Customer_gst.objects.all().exists():
            customerdata_gst = Customer_gst.objects.all().count()
            customer_id = customerdata_gst + 1
        else:
            customer_id = 1
    
    context = {
        'customer_id':customer_id
    }
    return render(request,"customer/addcustomer.html",context)
    
@login_required(login_url='login')
def viewcustomer(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            customer_data = Customer_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            customer_data = Customer_gst.objects.all()

        context = {
            'customer_data':customer_data
        }
        return render(request,"customer/viewcustomer.html",context)
    except:
        return redirect('error404')
    
@login_required(login_url='login')
def updatecustomer(request,pk):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
            customer = Customer_estimate.objects.get(pk=pk)

            customer.fullname = request.POST['fullname']
            customer.customerid = request.POST['customerid']
            customer.contactno = request.POST['mobile']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.landmark = request.POST['landmark']

            customer.save()
            messages.success(request,"Update Customer Successfully ! ")
            return redirect('viewcustomer')
        
        if request.user.groups.filter(name='GST').exists():
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
            return redirect('viewcustomer')

    if request.user.groups.filter(name='Estimate').exists():
        customer_data = Customer_estimate.objects.get(pk=pk)


    if request.user.groups.filter(name='GST').exists():
        customer_data = Customer_gst.objects.get(pk=pk)

    context = {
        'customer_data':customer_data
    }
    return render(request,"customer/updatecustomer.html",context)