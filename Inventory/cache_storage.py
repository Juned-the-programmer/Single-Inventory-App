from django.core.cache import cache
from supplier.models import *
from products.models import *
from customer.models import *

def supplier_cache():
    cache_key = "supplier_data_estimate_cache"
    cache_supplier_data = cache.get(cache_key)

    if cache_supplier_data is None:
        Supplier_data = Supplier_estimate.objects.all()
        cache.set(cache_key, Supplier_data , timeout=None)
        print("Supplier Non Cache Data")
    else:
        Supplier_data = cache_supplier_data
        print("Supplier Cached Data")

    return Supplier_data

def product_cache():
    cache_key = "product_data_estimate_cache" 
    cached_productdata = cache.get(cache_key)
        
    if cached_productdata is None:
        productdata = Product_estimate.objects.all()
        cache.set(cache_key, productdata, timeout=None)
        print("Product Non Cached Data")
    else:
        product_data = cached_productdata
        print("Product cached Data")
    
    return product_data
    
def customer_cache():
    cache_key = "customer_data_estimate_cache"
    cache_customer_data = cache.get(cache_key)

    if cache_customer_data is None:
        customer_data = Customer_estimate.objects.all()
        cache.set(cache_key, customer_data , timeout = None)
        print("Customer Non Cahce Data")
    else:
        customer_data = cache_customer_data
        print("Customer Cache Data")

    return customer_data

def customer_cache_gst():
    cache_key = "gst_customer_data_cache"
    cache_customer_data = cache.get(cache_key)

    if cache_customer_data is None:
        customer_data = Customer_gst.objects.all()
        cache.set(cache_key, customer_data, timeout=None)
        print("GST Customer Non Cache Data")
    else:
        customer_data = cache_customer_data
        print("GST Customer Cache Data")

    return customer_data

def product_cache_gst():
    cache_key = "gst_product_data_cache"
    cache_product_data = cache.get(cache_key)

    if cache_product_data is None:
        product_data = Product_gst.objects.all()
        cache.set(cache_key, product_data, timeout=None)
        print("GST Product Non Cache Data")
    else:
        product_data = cache_product_data
        print("GST Product Cache Data")
    
    return product_data
    
def supplier_cache_gst():
    cache_key = "gst_supplier_data_cache"
    cache_supplier_data = cache.get(cache_key)

    if cache_supplier_data is None:
        supplier_data = Supplier_gst.objects.all()
        cache.set(cache_key, supplier_data, timeout=None)
        print("GST Supplier Non Cache Data")
    else:
        supplier_data = cache_supplier_data
        print("GST Supplier Cache Data")

    return supplier_data