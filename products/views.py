from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from .models import *
from Inventory.cache_storage import *
import json

''' To add / view and update Product details '''

# To add Product
@login_required(login_url='login')
def addproduct(request):
    if request.method == 'POST' and 'Add Category' in request.POST:
        category = product_category(
            product_category = request.POST['category']
        )
        category.save()

    if request.method == 'POST' and 'Estimate' in request.POST:
        # Check for User Group
        if request.session['Estimate']:
            supplier_id = request.POST.get('supplier')
            supplier = None
            if supplier_id:
                supplier = Supplier_estimate.objects.get(id=supplier_id)

            purchase_price_str = request.POST.get('purchaseprice', 0.0)
            purchase_price = float(purchase_price_str) if purchase_price_str else 0.0

            if request.session["Manufacture"]:
                is_manufacturing_product = request.POST['radio-inline']
                is_manufacturing = is_manufacturing_product == "yes"

                if is_manufacturing:
                    product_type = Product_type.objects.get(product_type="Manufacture")
                else:
                    product_type = None

            product = Product_estimate(
                product_name = request.POST['productname'],
                product_categ = product_category.objects.get(id=request.POST['category']),
                unit = request.POST['unit'],
                selling_price = request.POST['sellingprice'],
                store_location = request.POST['storelocation'],
                supplier = supplier,
                minimum_stock =  request.POST['minimum_stock'],
                purchase_price = purchase_price,
            )

            if request.session['Manufacture']:
                product.product_type = product_type

            # save
            product.save()
            messages.success(request, "Product Addedd Successfully ! ")

            # Populate the new value to caching by refreshing the entire chache
            cache_product_data()
            
        # Check for user Group
        if request.session['GST']:
            product = Product_gst(
                product_name = request.POST['productname'],
                product_categ = request.POST['productcategory'],
                unit = request.POST['unit'],
                selling_price = request.POST['sellingprice'],
                store_location = request.POST['storelocation'],
                supplier = Supplier_gst.objects.get(fullname=request.POST['supplier']),
                minimum_stock =  request.POST['minimum_stock']
            )
            # Save
            product.save()
            messages.success(request , "Product Addedd Successfully ! ")

    # check for user Group
    if request.session['Estimate']:
        # Get all the supplier data Estimate
        Supplier_data = supplier_cache()

        category = product_category.objects.all()

    # Check for User Group        
    if request.session['GST']:
        # Get all the supplier data
        Supplier_data = Supplier_gst.objects.all()

    context = {
        'Supplier_data':Supplier_data,
        'category' : category
    }
    return render(request,"products/addproduct.html",context)

# To view products
@login_required(login_url='login')
def viewproduct(request):
    try:
        # Check for user Group
        if request.session['Estimate']:
            # Get all the product data for Estimate
            Product_data = Product_estimate.objects.all().prefetch_related('product_categ')

        # Check for user Group            
        if request.session['GST']:
            # Get all the product data for GST
            Product_data = Product_gst.objects.all()
            
        context = {
            'Product_data' : Product_data
        }
        return render(request,"products/viewproduct.html",context)
    except:
        return redirect('error404')

# To update the product (request,pk) pk would be the Product ID
@login_required(login_url='login')
def updateproduct(request,pk):
    try:
        if request.method =='POST':
            # Check for User group
            if request.session['Estimate']:
                product = Product_estimate.objects.get(pk=pk)

                supplier_id = request.POST.get('supplier')
                supplier = None
                if supplier_id:
                    supplier = Supplier_estimate.objects.get(id=request.POST['supplier'])

                purchase_price_str = request.POST.get('purchaseprice', 0.0)
                purchase_price = float(purchase_price_str) if purchase_price_str else 0.0

                is_manufacturing_product = request.POST['radio-inline']
                is_manufacturing = is_manufacturing_product == "yes"
                
                if is_manufacturing:
                    product_type = Product_type.objects.get(product_type="Manufacture")
                else:
                    product_type = None

                product.product_name = request.POST['productname']
                product.product_categ = request.POST['productcategory']
                product.unit  = request.POST['unit']
                product.selling_price = request.POST['sellingprice']
                product.store_location = request.POST['storelocation']
                product.supplier = supplier
                product.purchase_price = purchase_price
                product.minimum_stock = request.POST['minimum_stock']
                product.product_type = product_type

                # Save
                product.save()
                messages.success(request, "Product Updated Successfully ! ")

            if request.session['GST']:
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
        
        if request.session['Estimate']:
            product_data = product_cache()
            Product_data = product_data.get(pk=pk)
        
            supplier_data = supplier_cache()
        
        if request.session['GST']:
            Product_data = Product_gst.objects.get(pk=pk)
            supplier_data = Supplier_gst.objects.all()

        context = {
            'Product_data' : Product_data,
            'supplier_data' :  supplier_data
        }
        return render(request,"products/updateproduct.html",context)
    except:
        return redirect('error404')

@login_required(login_url='login')
def manufacture_product(request):
    if request.session["Manufacture"] and request.session["Estimate"]:
        if request.method == 'POST':
            selected_products = request.POST.get('selected_product_data')
            if selected_products:
                # Parse JSON object
                selected_products = json.loads(selected_products)
                # Load Stock data
                stock_detail = Stock_estimate.objects.all()

                product_data = stock_detail.get(product = request.POST['manufacture_product'])
                product_data.quantity += int(request.POST['manufacture_quantity'])
                product_data.save()
                

                for product_pair in selected_products:
                    stock_data = stock_detail.get(product=Product_estimate.objects.get(id=product_pair['productId']))
                    stock_data.quantity -= int(product_pair['quantity'])
                    stock_data.save()

                messages.success(request, "Product Manufactured Successfully ! ")

    product_data = product_cache()

    product_type = Product_type.objects.get(product_type="Manufacture")

    product_manufacture = product_data.filter(product_type=product_type.id)

    context = {
        'product_manufacture' : product_manufacture
    }
    return render(request, 'products/addmanufactureproduct.html', context)

@login_required(login_url='login')
def product_required_manufacture(request):
    product_name = request.GET['manufacture_product']
    product_detail = product_required_to_manufacture.objects.get(manufacture_product = product_name)
    product_data = product_detail.required_products.all()
    return JsonResponse({"Product_data":list(product_data.values())})


@login_required(login_url='login')
def product_required(request):
    if request.session["Manufacture"] and request.session["Estimate"]:
        if request.method == 'POST':
            selected_products = request.POST.get('selected_products')
            if selected_products:
                # Parse the JSON data from the hidden field
                selected_products = json.loads(selected_products)
                
                # Intialize an Empty Array
                required_product = []

                # Loop through the selected products and create product_required_to_manufacture instances
                for product_pair in selected_products:
                    required_product_id = product_pair['requiredProduct']
                    required_product.append(Product_estimate.objects.get(id=required_product_id))

                product_required_manufacture = product_required_to_manufacture(
                    manufacture_product = Product_estimate.objects.get(id=request.POST['manufactured_product']),
                    desciption = request.POST['manufacture_description']
                )
                product_required_manufacture.save()

                product_required_manufacture.required_products.set(required_product)
                product_required_manufacture.save()

    product_data = product_cache()

    product_type = Product_type.objects.get(product_type="Manufacture")

    Manufacured_products = product_data.filter(product_type=product_type.id)
    Required_products = product_data.exclude(product_type=product_type.id)
    context = {
        'manufactured_product' : Manufacured_products,
        'required_products' : Required_products
    }
    return render(request, 'products/productrequiredtomanufacture.html', context)

''' This is used to update the cache detail. 
When we add new product then it will update the cache to new details of all the product data '''
def cache_product_data():
    cache_key = "product_data_estimate_cache"
    product_data = Product_estimate.objects.all()
    cache.set(cache_key, product_data, timeout=None)