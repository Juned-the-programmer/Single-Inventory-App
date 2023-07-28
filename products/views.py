from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,  User
from .models import *
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def addproduct(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if "Estimate" in request.POST:
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
                else:
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

            if Estimate_group in user.groups.all():
                Supplier_data = Supplier_estimate.objects.all()
            if GST_group in user.groups.all():
                Supplier_data = Supplier_gst.objects.all()

            context = {
                'Supplier_data':Supplier_data
            }
            return render(request,"products/addproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def viewproduct(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if Estimate_group in user.groups.all():
                Product_data = Product_estimate.objects.all()
            if GST_group in user.groups.all():
                Product_data = Product_gst.objects.all()
            context = {
                'Product_data' : Product_data
            }
            return render(request,"products/viewproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')

@login_required(login_url='login')
def updateproduct(request,pk):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method =='POST':
                if Estimate_group in user.groups.all():
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

                if GST_group in user.groups.all():
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
            
            if Estimate_group in user.groups.all():
                Product_data = Product_estimate.objects.get(pk=pk)
                supplier_data = Supplier_estimate.objects.all()
            
            if GST_group in user.groups.all():
                Product_data = Product_gst.objects.get(pk=pk)
                supplier_data = Supplier_gst.objects.all()

            context = {
                'Product_data' : Product_data,
                'supplier_data' :  supplier_data
            }
            return render(request,"products/updateproduct.html",context)
        else:
            return redirect('login')
    except:
        return redirect('error404')