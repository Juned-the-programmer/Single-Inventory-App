from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *


# Create your views here.
@login_required(login_url='login')
def addproduct(request):
    try:
        if request.method == 'POST':
            if request.user.groups.filter(name='Estimate').exists():
                product = Product_estimate(
                    product_name = request.POST['productname'],
                    product_categ = request.POST['productcategory'],
                    unit = request.POST['unit'],
                    selling_price = request.POST['sellingprice'],
                    store_location = request.POST['storelocation'],
                    supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier']),
                    minimum_stock =  request.POST['minimum_stock']
                )
                product.save()
                messages.success(request, "Product Addedd Successfully ! ")
            
            if request.user.groups.filter(name='GST').exists():
                product = Product_gst(
                    product_name = request.POST['productname'],
                    product_categ = request.POST['productcategory'],
                    unit = request.POST['unit'],
                    selling_price = request.POST['sellingprice'],
                    store_location = request.POST['storelocation'],
                    supplier = Supplier_gst.objects.get(fullname=request.POST['supplier']),
                    minimum_stock =  request.POST['minimum_stock']
                )
                product.save()
                messages.success(request , "Product Addedd Successfully ! ")

        if request.user.groups.filter(name='Estimate').exists():
            Supplier_data = Supplier_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            Supplier_data = Supplier_gst.objects.all()

        context = {
            'Supplier_data':Supplier_data
        }
        return render(request,"products/addproduct.html",context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def viewproduct(request):
    try:
        if request.user.groups.filter(name='Estimate').exists():
            Product_data = Product_estimate.objects.all()
            
        if request.user.groups.filter(name='GST').exists():
            Product_data = Product_gst.objects.all()
            
        context = {
            'Product_data' : Product_data
        }
        return render(request,"products/viewproduct.html",context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def updateproduct(request,pk):
    try:
        if request.method =='POST':
            if request.user.groups.filter(name='Estimate').exists():
                product = Product_estimate.objects.get(pk=pk)

                product.product_name = request.POST['productname']
                product.product_categ = request.POST['productcategory']
                product.unit  = request.POST['unit']
                product.selling_price = request.POST['sellingprice']
                product.store_location = request.POST['storelocation']
                product.supplier = Supplier_estimate.objects.get(fullname=request.POST['supplier'])
                product.minimum_stock = request.POST['minimum_stock']
                product.save()
                messages.success(request, "Product Updated Successfully ! ")

            if request.user.groups.filter(name='GST').exists():
                product = Product_gst.objects.get(pk=pk)

                product.product_name = request.POST['productname']
                product.product_categ = request.POST['productcategory']
                product.unit = request.POST['unit']
                product.selling_price = request.POST['sellingprice']
                product.store_location = request.POST['storelocation']
                product.supplier = Supplier_gst.objects.get(fullname=request.POST['supplier'])
                product.minimum_stock = request.POST['minimum_stock']
                product.save()
                messages.success(request , "Product Updated Successfully ! ")
        
        if request.user.groups.filter(name='Estimate').exists():
            Product_data = Product_estimate.objects.get(pk=pk)
            supplier_data = Supplier_estimate.objects.all()
        
        if request.user.groups.filter(name='GST').exists():
            Product_data = Product_gst.objects.get(pk=pk)
            supplier_data = Supplier_gst.objects.all()

        context = {
            'Product_data' : Product_data,
            'supplier_data' :  supplier_data
        }
        return render(request,"products/updateproduct.html",context)
    except:
        return redirect('error404')