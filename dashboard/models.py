from django.db import models
from django.db.models.signals import post_save
# Create your models here.
class Customer_estimate(models.Model):
    customerid = models.IntegerField()
    fullname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname

class customeraccount_estimate(models.Model):
    customer_name = models.ForeignKey(Customer_estimate,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.customer_name.fullname)

class customerpay_estimate(models.Model):
    customer_name = models.ForeignKey(Customer_estimate , on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    Description = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.customer_name.fullname)

class Customer_gst(models.Model):
    customerid = models.IntegerField()
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contactno = models.CharField(max_length=50)
    gst = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname

class customeraccount_gst(models.Model):
    customer_name = models.ForeignKey(Customer_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.customer_name.fullname)

class customerpay_gst(models.Model):
    customer_name = models.ForeignKey(Customer_gst , on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    Description = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.customer_name.fullname)

class Supplier_estimate(models.Model):
    supplierid = models.IntegerField()
    fullname = models.CharField(max_length=50)
    contactno = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname

class supplieraccount_estimate(models.Model):
    supplier_name = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    amount = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.supplier_name.fullname)

class supplierpay_estimate(models.Model):
    supplier_name = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.supplier_name.fullname)

class Supplier_gst(models.Model):
    supplierid = models.IntegerField()
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contactno = models.CharField(max_length=50)
    gst = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname

class supplieraccount_gst(models.Model):
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
    amount = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.supplier_name.fullname)

class supplierpay_gst(models.Model):
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
    pending_amount = models.FloatField()
    paid_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.supplier_name.fullname)

class Product_estimate(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_estimate , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()

    def __str__(self):
        return self.product_name

class Stock_estimate(models.Model):
    product = models.OneToOneField(Product_estimate,on_delete=models.CASCADE)    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return str(self.product.product_name)

class Product_gst(models.Model):
    product_name = models.CharField(max_length=100)
    product_categ = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    selling_price = models.FloatField()
    store_location = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier_gst , on_delete=models.CASCADE , blank=True,null=True)
    minimum_stock=models.IntegerField()

    def __str__(self):
        return self.product_name

class Stock_gst(models.Model):
    product = models.OneToOneField(Product_gst,on_delete=models.CASCADE)    
    quantity = models.IntegerField(null=True,blank=True,default=0)
    purchase_price = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return str(self.product.product_name)

class Estimate_Purchase(models.Model):
    Bill_no = models.IntegerField()
    supplier = models.ForeignKey(Supplier_estimate,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    Total_amount = models.FloatField()
    Due_amount = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()

    def __str__(self):
        return str(self.Bill_no)

class estimatepurchase_Product(models.Model):
    Bill_no = models.IntegerField()
    # product_name = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    dis = models.FloatField()
    netrate = models.FloatField()
    total = models.FloatField()
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.Bill_no)

class GST_Purchase(models.Model):
    Bill_no = models.IntegerField()
    supplier_name = models.ForeignKey(Supplier_gst,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    CGST = models.FloatField()
    SGST = models.FloatField()
    IGST = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()

    def __str__(self):
        return str(self.Bill_no)

class gstpurchase_Product(models.Model):
    Bill_no = models.IntegerField()
    hsncode=models.IntegerField()
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    gstp = models.FloatField()
    gstamt = models.FloatField()
    total = models.FloatField()
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.Bill_no)

class Estimate_sales(models.Model):
    Bill_no = models.IntegerField()
    customer = models.ForeignKey(Customer_estimate,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    Total_amount = models.FloatField()
    Due_amount = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()

    def __str__(self):
        return str(self.Bill_no)
    
class estimatesales_Product(models.Model):
    Bill_no = models.IntegerField()
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    dis = models.FloatField()
    netrate = models.FloatField()
    total = models.FloatField()
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.Bill_no)

class gstsale(models.Model):
    Bill_no = models.IntegerField()
    customer_name =  models.ForeignKey(Customer_gst,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    CGST = models.FloatField()
    SGST = models.FloatField()
    IGST = models.FloatField()
    Round_off = models.FloatField()
    Grand_total = models.FloatField()

    def __str__(self):
        return str(self.Bill_no)

class gstsales_Product(models.Model):
    Bill_no = models.IntegerField()
    hsncode=models.IntegerField()
    product_name = models.CharField(max_length=100,null=True,blank=True)
    unit = models.CharField(max_length=10)
    rate = models.FloatField()
    qty= models.IntegerField()
    gstp = models.FloatField()
    gstamt = models.FloatField()
    total = models.FloatField()
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.Bill_no)

class dailyincome_estimate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class dailyincome_gst(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class dailyexpense_estimate(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

class dailyexpense_gst(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

class category_estimate(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class category_gst(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name

def create_stock_estimate(sender,instance,created,**kwargs):
    if created:
        Stock_estimate.objects.create(product=instance)

def create_stock_gst(sender,instance,created,**kwargs):
    if created:
        Stock_gst.objects.create(product=instance)
        
def create_customer_account_estimate(sender,instance,created,**kwargs):
    if created:
        customeraccount_estimate.objects.create(customer_name=instance)

def create_customer_account_gst(sender,instance,created,**kwargs):
    if created:
        customeraccount_gst.objects.create(customer_name=instance)
        
def create_supplier_account_estimate(sender,instance,created,**kwargs):
    if created:
        supplieraccount_estimate.objects.create(supplier_name=instance)

def create_supplier_account_gst(sender,instance,created,**kwargs):
    if created:
        supplieraccount_gst.objects.create(supplier_name=instance)

post_save.connect(create_supplier_account_estimate,sender=Supplier_estimate)
post_save.connect(create_supplier_account_gst,sender=Supplier_gst)
post_save.connect(create_customer_account_estimate,sender=Customer_estimate)
post_save.connect(create_customer_account_gst,sender=Customer_gst)
post_save.connect(create_stock_estimate,sender=Product_estimate)
post_save.connect(create_stock_gst,sender=Product_gst)