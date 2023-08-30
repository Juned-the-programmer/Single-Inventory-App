import datetime
import itertools
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import redirect, render
from num2words import num2words
from django.db.models import F

from customer.models import *
from pages.models import *
from products.models import *
from purchase.models import *
from sales.models import *
from supplier.models import *
from .models import *

# Create your views here

# Get the data which need to be diplayed at the home page dashboard.
''' The data comes from the dashborad_data_estimate model which is continuosly updating as we are adding the records into the purchase and sale '''
@login_required(login_url='login')
def dashboard(request):
    if request.user.groups.filter(name='Estimate').exists():
        # Loaded dashboard data 
        dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")

        # Customer Count
        Customer_data = dashboard_data.total_customer_count

        # Supplier Count
        Supplier_data = dashboard_data.total_supplier_count

        # Product Count
        Product_data = dashboard_data.total_product_count

        # Today sale
        today_sale = dashboard_data.today_estimate_sale

        # Current Month Sale
        current_month_sale = dashboard_data.current_month_estimate_sale

        # Previous Month Sale
        previous_month_sale = dashboard_data.previous_month_estimate_sale

        # Today Purchase
        today_purchase = dashboard_data.today_estimate_purchase

        # Current Month Purchase
        current_month_purchase = dashboard_data.current_month_estimate_purchase

        # Previous Month Purchase
        previous_month_total_purchase = dashboard_data.previous_month_estimate_purchase

        #Current Month Profit
        current_month_profit = dashboard_data.current_month_profit

        #Previous Month Profit
        previous_month_profit = dashboard_data.previous_month_profit

        #Total
        total_profit = dashboard_data.total_profit

        #OutofStock
        stocks_with_min_quantity = Stock_estimate.objects.annotate(min_stock=F('product__minimum_stock')).filter(quantity__lte=F('min_stock'))
        out_of_stock = stocks_with_min_quantity.count()

        #In stock data
        stock_data = Stock_estimate.objects.all().count()
        stock_data = int(stock_data) - int(out_of_stock)
        
        context = {
            'customerdata':Customer_data,
            'supplierdata':Supplier_data,
            'productdata':Product_data,
            'today_sale': today_sale,
            'current_month_sale':current_month_sale,
            'previous_month_sale':previous_month_sale,
            'today_purchase':today_purchase,
            'current_month_purchase':current_month_purchase,
            'previous_month_total_purchase':previous_month_total_purchase,
            'current_month_profit' : current_month_profit,
            'previous_month_profit' : previous_month_profit,
            'total_profit' : total_profit,
            'out_of_stock' : out_of_stock,
            'remaining_stock_data' : stock_data
        }
        return render(request,"dashboard/dashboard.html",context)
    
    if request.user.groups.filter(name='GST').exists():
        sale = 0
        Customer_data = Customer_gst.objects.all().count()
        print(Customer_data)
        Supplier_data = Supplier_gst.objects.all().count()
        print(Supplier_data)
        Product_data = Product_gst.objects.all().count()
        print(Product_data)

        #Today GST Sale
        today_sale = 0
        now = date.today()
        month = now.month
        year = now.year
        day = now.day
        total_sale_record = gstsale.objects.all().count()
        today_sale_record = gstsale.objects.filter(date__day=day,date__month=month,date__year=year).count()
        totalsale = gstsale.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Grand_total'))
        round_off = gstsale.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
        total_sale = totalsale['Grand_total__sum']
        roundoff = round_off['Round_off__sum']
        if today_sale_record == 0:
            print("Estimate Sale Total")
        else:
            today_sale = float(total_sale) - float(roundoff)
            print("Today_Sale")

        # Total GST Sale
        totalsale = gstsale.objects.aggregate(Sum('Grand_total'))
        round_off = gstsale.objects.aggregate(Sum('Round_off'))
        total_sale = totalsale['Grand_total__sum']
        roundoff = round_off['Round_off__sum']
        if total_sale_record == 0:
            print("Total Estimate Sale")
        else:
            sale = float(total_sale) - float(roundoff)

        #Current Month GST Sale
        current_month_sale = 0
        current_total = gstsale.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Grand_total'))
        current_roundoff = gstsale.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
        current_total_sale = current_total['Grand_total__sum']
        current_roundoff_sale = current_roundoff['Round_off__sum']
        if total_sale_record == 0:
            print("Current Month Estimate Sale")
        else:
            current_month_sale = float(current_total_sale) - float(current_roundoff_sale)

        #Previous Month GST Sale  
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        lastyear = lastMonth.strftime("%Y")
        lastmonth = lastMonth.strftime("%m")
        previous_month_sale = 0
        previous_total_count = gstsale.objects.filter(date__month=lastmonth,date__year=lastyear).count()
        if previous_total_count == 0:
            print("Previous Month Estimate Sale")
        else:
            previous_total = gstsale.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Grand_total'))
            previous_roundoff = gstsale.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Round_off'))
            previous_total_sale = previous_total['Grand_total__sum']
            previous_roundoff_sale = previous_roundoff['Round_off__sum']
            previous_month_sale = float(previous_total_sale) - float(previous_roundoff_sale)          

        #Today GST Purchase
        today_purchase = 0
        now = date.today()
        month = now.month
        year = now.year
        day = now.day
        total_purchase_record = GST_Purchase.objects.all().count()
        today_purchase_record = GST_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).count()
        totalpurchase = GST_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Grand_total'))
        purchase_round_off = GST_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
        total_purchase = totalpurchase['Grand_total__sum']
        purchaseroundoff = purchase_round_off['Round_off__sum']
        if total_purchase_record == 0:
            print("Estimate Sale Total")
        elif today_purchase_record == 0:
            print("Estimate Today Sale")
        else:
            today_purchase = float(total_purchase) - float(purchaseroundoff)

        #Current Month Estimate Purchase
        total_purchase_record = GST_Purchase.objects.all().count()
        current_month_purchase = 0
        current_total_purchase = GST_Purchase.objects.filter(date__month=month,date__year=year).aggregate(Sum('Grand_total'))
        current_roundoff_purchase = GST_Purchase.objects.filter(date__month=month,date__year=year).aggregate(Sum('Round_off'))
        current_total_eatimate_purchase = current_total_purchase['Grand_total__sum']
        current_roundoff_estimate_purchase = current_roundoff_purchase['Round_off__sum']
        if total_purchase_record == 0:
            print("Current Month Estimate Purchase")
        elif today_purchase_record == 0:
            print("Current Month Estimate Purchase")
        else:
            current_month_purchase = float(current_total_eatimate_purchase) - float(current_roundoff_estimate_purchase)

        # Previous Month Estimate Purchase
        previous_month_total_purchase = 0
        previous_total_purchase_count = GST_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).count()
        if previous_total_purchase_count == 0:
            print("Previous Month Estimate Purchase")
        else:
            previous_purchase_total = GST_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Grand_total'))
            previous_purchase_roundoff = GST_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Round_off'))
            previous_total_purchase = previous_purchase_total['Grand_total__sum']
            previous_roundoff_purchase = previous_purchase_roundoff['Round_off__sum']
            previous_month_total_purchase = float(previous_total_purchase) - float(previous_roundoff_purchase)

        #Total Estimate Purchase
        Total_Eatimate_Purchase = 0
        if total_purchase_record == 0:
            print("Total Estimate Purchase")
        else:
            total_estimate_purchase = GST_Purchase.objects.all().aggregate(Sum('Grand_total'))
            roundoff_estimate_purchase = GST_Purchase.objects.all().aggregate(Sum('Round_off'))
            estimate_purchase = total_estimate_purchase['Grand_total__sum']
            estimate_roundoff = roundoff_estimate_purchase['Round_off__sum']
            Total_Eatimate_Purchase = float(estimate_purchase) - float(estimate_roundoff)

        #Current Month Profit
        current_month_profit = current_month_sale - current_month_purchase

        #Previous Month Profit
        previous_month_profit = previous_month_sale - previous_month_total_purchase

        #Total
        total_profit = sale - Total_Eatimate_Purchase
        
        context = {
            'customerdata':Customer_data,
            'supplierdata':Supplier_data,
            'productdata':Product_data,
            'today_sale': today_sale,
            'current_month_sale':current_month_sale,
            'previous_month_sale':previous_month_sale,
            'today_purchase':today_purchase,
            'current_month_purchase':current_month_purchase,
            'previous_month_total_purchase':previous_month_total_purchase,
            'Total_Eatimate_Purchase':Total_Eatimate_Purchase,
            'current_month_profit' : current_month_profit,
            'previous_month_profit' : previous_month_profit,
            'total_profit' : total_profit
        }
        return render(request,"dashboard/dashboard.html",context)