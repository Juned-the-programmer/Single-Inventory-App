import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.core.cache import cache

from .models import *
from Inventory.cache_storage import *

# Method to check weather the ID what we have generated is Unique all over the database.
def is_unique_id_unique(unique_id, request):
    #Check for the Unique ID
    if request.session['Estimate']:
        from .models import Customer_estimate
        return not Customer_estimate.objects.filter(customer_id=unique_id).exists()
    
    if request.session['GST']:
        from .models import Customer_gst
        return not Customer_gst.objects.filter(customerid=unique_id).exists()

# Generate the Unique ID for every customer based on the customer full name [first name and last name]
''' Usage: 
It will generate the Unique ID for every customer what we are adding into the database. 
It will extract the frrst_name and last_name from the full name and along side of that it use 4 randm number.
Once this is assign never get change. '''
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
    
# Adding customer detail.
@login_required(login_url='login')
def addcustomer(request):
    if request.method == 'POST':
        # Check for weather the request is from Estimate or GST.
        if request.session['Estimate']:
            # Generating the customer object
            customer = Customer_estimate(
                customer_id=generate_unique_id(request.POST['fullname'], request),
                fullname = request.POST['fullname'],
                contactno = request.POST['mobile'],
                city = request.POST['city'],
                state = request.POST['state'],
                landmark = request.POST['landmark']
            )
            # Save
            customer.save()
            messages.success(request , "Added Customer Successfully ! ")

            cache.delete("customer_data_estimate_cache")
            customer_cache()
        
        # Check for weather the request is from Estimate or GST.
        if request.session['GST']:
            # Generating Customer Object
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
            # Save
            customer.save()
            messages.success(request, "Added Customer Successfully ! ")

            cache.delete("gst_customer_data_cache")
            customer_cache_gst()

    context = {}

    return render(request,"customer/addcustomer.html", context)
    
@login_required(login_url='login')
def viewcustomer(request):
    try:
        # Check for weather the request is from Estimate or GST.
        if request.session['Estimate']:
            customer_data = customer_cache()
        
        # Check for weather the request is from Estimate or GST.
        if request.session['GST']:
            customer_data = customer_cache_gst()

        context = {
            'customer_data':customer_data
        }
        return render(request,"customer/viewcustomer.html",context)
    except:
        return redirect('error404')

# Updating customer (request,pk) pk stands for customer ID for that record [uuid] not the one which we have generated.
@login_required(login_url='login')
def updatecustomer(request,pk):
    if request.method == 'POST':
        # Check for weather the request is from Estimate or GST.
        if request.session['Estimate']:

            customer_data = customer_cache()
            customer = customer_data.get(pk=pk)

            customer.fullname = request.POST['fullname']
            customer.contactno = request.POST['mobile']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.landmark = request.POST['landmark']

            customer.save()
            messages.success(request,"Update Customer Successfully ! ")

            cache.delete("customer_data_estimate_cache")
            customer_cache()
        
        # Check for weather the request is from Estimate or GST.
        if request.session['GST']:

            customer_data = customer_cache_gst()
            customer = customer_data.get(pk=pk)

            customer.fullname = request.POST['fullname']
            customer.contactno = request.POST['mobile']
            customer.gst = request.POST['gstno']
            customer.email = request.POST['email']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.landmark = request.POST['landmark']

            customer.save()
            messages.success(request, "Update Customer Successfully ! ")

            cache.delete("gst_customer_data_cache")
            customer_cache_gst()

    ''' To get the data from the datbase and and poplate that into the template for updating details '''
    # Check for weather the request is from Estimate or GST.
    if request.session['Estimate']:
        customer_data = customer_cache()
        customer_data = customer_data.get(id=pk)

    # Check for weather the request is from Estimate or GST.
    if request.session['GST']:
        customer_data = customer_cache_gst()
        customer_data = customer_data.get(id=pk)

    context = {
        'customer_data':customer_data
    }
    return render(request,"customer/updatecustomer.html",context)