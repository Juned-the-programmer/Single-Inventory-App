import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.core.cache import cache

from .models import *

# Method to check weather the ID what we have generated is Unique all over the database.
def is_unique_id_unique(unique_id, request):
    #Check for the Unique ID
    if request.user.groups.filter(name='Estimate').exists():
        from .models import Supplier_estimate
        return not Supplier_estimate.objects.filter(supplier_id=unique_id).exists()
    
    if request.user.groups.filter(name='GST').exists():
        from .models import Supplier_gst
        return not Supplier_gst.objects.filter(supplierid=unique_id).exists()

# Generate the Unique ID for every customer based on the customer full name [first name and last name]
''' Usage: 
It will generate the Unique ID for every supplier what we are adding into the database. 
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

# To add the Supplier data.
@login_required(login_url='login')
def addsupplier(request):
    if request.method == 'POST':
        # Check for User Group
        if request.user.groups.filter(name='Estimate').exists():
            # Creating object
            supplier = Supplier_estimate(
                supplier_id=generate_unique_id(request.POST['fullname'], request),
                fullname = request.POST['fullname'],
                contactno = request.POST['mobile'],
                city = request.POST['city'],
                state = request.POST['state'],
                landmark = request.POST['landmark']
            )
            # Save
            supplier.save()
            messages.success(request , "Added Supplier Successfully ! ")

            cache_supplier_data()
        
        # Check for User Group
        if request.user.groups.filter(name='GST').exists():
            # Creating object
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
            # Save
            supplier.save()
            messages.success(request, "Added Supplier Successfully ! ")
    
    context = {}
    
    return render(request,"supplier/addsupplier.html",context)


 # To view supplier
@login_required(login_url='login')
def viewsupplier(request):
    try:
        # Check for user Group
        if request.user.groups.filter(name='Estimate').exists():
            # To get all the supplier data
            cache_key = "supplier_data_estimate_cache"
            cache_supplier_data = cache.get(cache_key)

            if cache_supplier_data is None:
                supplier_data = Supplier_estimate.objects.all()
                cache.set(cache_key, supplier_data , timeout = None)
            else:
                supplier_data = cache_supplier_data

        # Check for user Group
        if request.user.groups.filter(name='GST').exists():
            # To get all the supplier data
            supplier_data = Supplier_gst.objects.all()

        context = {
            'supplier_data': supplier_data
        }
        return render(request,"supplier/viewsupplier.html",context)
    except:
        return redirect('error404')

# To update the supplier details.
@login_required(login_url='login')
def updatesupplier(request,pk):
    try:
        if request.method == 'POST':
            # Check for user Group
            if request.user.groups.filter(name='Estimate').exists():
                # Get the supplier details
                supplier = Supplier_estimate.objects.get(pk=pk)

                # Update the values
                supplier.fullname = request.POST['fullname']
                supplier.customerid = request.POST['customerid']
                supplier.contactno = request.POST['mobile']
                supplier.city = request.POST['city']
                supplier.state = request.POST['state']
                supplier.landmark = request.POST['landmark']

                # Save
                supplier.save()
                messages.success(request,"Update Supplier Successfully ! ")

                cache_supplier_data()
            
            # Check for user Group
            if request.user.groups.filter(name='GST').exists():
                # Get the supplier details
                supplier = Supplier_gst.objects.get(pk=pk)

                # Update the values
                supplier.fullname = request.POST['fullname']
                supplier.customerid = request.POST['customerid']
                supplier.contactno = request.POST['mobile']
                supplier.gst = request.POST['gstno']
                supplier.email = request.POST['email']
                supplier.city = request.POST['city']
                supplier.state = request.POST['state']
                supplier.landmark = request.POST['landmark']

                # Save
                supplier.save()
                messages.success(request, "Update Supplier Successfully ! ")
        
        # Check for user Group
        if request.user.groups.filter(name='Estimate').exists():
            # Get the supplier detail
            cache_key = "supplier_data_estimate_cache"
            cache_supplier_data = cache.get(cache_key)

            if cache_supplier_data is None:
                supplier_data = Supplier_estimate.objects.all()
                cache.set(cache_key, supplier_data , timeout = None)
            else:
                supplier_data = cache_supplier_data

            supplier_data = supplier_data.get(id=pk)

        # Check for user Group
        if request.user.groups.filter(name='GST').exists():
            # Get the supplier details
            supplier_data = Supplier_gst.objects.get(pk=pk)
            
        context = {
            'supplier_data':supplier_data
        }
        return render(request,"supplier/updatesupplier.html",context)
    except:
        return redirect('error404')

def cache_supplier_data():
    cache_key = "supplier_data_estimate_cache"
    supplier_data = Supplier_estimate.objects.all()
    cache.set(cache_key, supplier_data, timeout=None)