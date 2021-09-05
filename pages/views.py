from django.shortcuts import render , redirect ,HttpResponse
from django.contrib.auth.models import auth,User,Group
from django.contrib import messages
from .models import *
from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Min,Max,Avg
from datetime import date 
import datetime
# Create your views here.

def login(request):
    if request.method == 'POST':   
        user_login = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user_login is not None:
            auth.login(request,user_login)
            messages.success(request,"Login Successfull")
            return redirect('dashboard')
        else:
            print("Login Again")
            messages.error(request , "Invalid Username or Password")

    return render(request,"pages/login.html")

def signup_gst(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordrepeat']:
            user_signup = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
            user_signup.save()

            add_group = Group.objects.get(name='GST')
            add_group.user_set.add(user_signup)

            user_login = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
            if user_login is not None:
                auth.login(request,user_login)
            else:
                print("Signup Again")

            data = request.user.profile

            data.phone_no = request.POST['phoneno']
            data.company_name = request.POST['companyname']
            data.Address = request.POST['address']
            data.city = request.POST['city']
            data.pincode = request.POST['pincode']
            data.state = request.POST['state']
            data.GSTNO = request.POST['GSTNO']
            data.Bank_name = request.POST['Bank name']
            data.Bank_AC = request.POST['Bank AC']
            data.IFSC_Code = request.POST['IFSC_Code']
            data.Branch_name = request.POST['Branch name']

            data.save()
            print("Success")
            return redirect('dashboard')

    return render(request,"pages/signup_gst.html")

def signup_estimate(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordrepeat']:
            user_signup = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
            user_signup.save()
            
            add_group = Group.objects.get(name='Estimate')
            add_group.user_set.add(user_signup)

            user_login = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
            if user_login is not None:
                auth.login(request,user_login)
            else:
                print("Singup Again")

            data = request.user.profile

            data.phone_no = request.POST['phoneno']
            data.company_name = request.POST['companyname']
            data.Address = request.POST['address']
            data.city = request.POST['city']
            data.state = request.POST['state']
            data.pincode = request.POST['pincode']

            data.save()
            print("success")
            return redirect('dashboard')
    return render(request,"pages/signup-estimate.html")


@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'Estimate' in request.POST: 
                    
                    data = request.user.profile    
                    data.phone_no = request.POST['phoneno']
                    data.company_name = request.POST['companyname']
                    data.Address = request.POST['address']
                    data.city = request.POST['city']
                    data.pincode = request.POST['pincode']
                    data.state = request.POST['state']

                    data.save()
                    return redirect('dashboard')
                
                else:

                    data = request.user.profile
                    data.phone_no = request.POST['phoneno']
                    data.company_name = request.POST['companyname']
                    data.Address = request.POST['address']
                    data.city = request.POST['city']
                    data.pincode = request.POST['pincode']
                    data.state = request.POST['state']
                    data.GSTNO = request.POST['GSTNO']
                    data.Bank_name = request.POST['Bank name']
                    data.Bank_AC = request.POST['Bank AC']
                    data.IFSC_Code = request.POST['IFSC_Code']
                    data.Branch_name = request.POST['Branch name']

                    data.save()
                    return redirect('dashboard')
        else:
            return redirect('login')
    except:
        return redirect('error404')

    profile_data = request.user.profile
    context = {
        'profile_data' : profile_data
    }
    return render(request,"pages/profile.html",context)


@login_required(login_url='login')
def dashboard(request):
    Estimate_group = Group.objects.get(name="Estimate")
    GST_group = Group.objects.get(name="GST")
    user = User.objects.get(username=request.user.username)
    if user.is_authenticated:
        if Estimate_group in user.groups.all():
            sale = 0
            Customer_data = Customer_estimate.objects.all().count()
            print(Customer_data)
            Supplier_data = Supplier_estimate.objects.all().count()
            print(Supplier_data)
            Product_data = Product_estimate.objects.all().count()
            print(Product_data)

            #Today Estimate Sale
            today_sale = 0
            now = date.today()
            month = now.month
            year = now.year
            day = now.day
            total_sale_record = Estimate_sales.objects.all().count()
            today_sale_record = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).count()
            totalsale = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Total_amount'))
            round_off = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
            total_sale = totalsale['Total_amount__sum']
            roundoff = round_off['Round_off__sum']
            if today_sale_record == 0:
                print("Estimate Sale Total")
            else:
                today_sale = float(total_sale) - float(roundoff)
                print("Today_Sale")

            # Total Estimate Sale
            totalsale = Estimate_sales.objects.aggregate(Sum('Total_amount'))
            round_off = Estimate_sales.objects.aggregate(Sum('Round_off'))
            total_sale = totalsale['Total_amount__sum']
            roundoff = round_off['Round_off__sum']
            if total_sale_record == 0:
                print("Total Estimate Sale")
            else:
                sale = float(total_sale) - float(roundoff)

            #Current Month Estimate Sale
            current_month_sale = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).count()
            current_total = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Total_amount'))
            current_roundoff = Estimate_sales.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
            current_total_sale = current_total['Total_amount__sum']
            current_roundoff_sale = current_roundoff['Round_off__sum']
            if current_month_sale == 0:
                print("Current Month Estimate Sale")
            else:
                current_month_sale = float(current_total_sale) - float(current_roundoff_sale)

            #Previous Month Estimate Sale  
            today = datetime.date.today()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            lastyear = lastMonth.strftime("%Y")
            lastmonth = lastMonth.strftime("%m")
            previous_month_sale = 0
            previous_total_count = Estimate_sales.objects.filter(date__month=lastmonth,date__year=lastyear).count()
            if previous_total_count == 0:
                print("Previous Month Estimate Sale")
            else:
                previous_total = Estimate_sales.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Total_amount'))
                previous_roundoff = Estimate_sales.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Round_off'))
                previous_total_sale = previous_total['Total_amount__sum']
                previous_roundoff_sale = previous_roundoff['Round_off__sum']
                previous_month_sale = float(previous_total_sale) - float(previous_roundoff_sale)          

            #Today Estimate Purchase
            today_purchase = 0
            now = date.today()
            month = now.month
            year = now.year
            day = now.day
            total_purchase_record = Estimate_Purchase.objects.all().count()
            today_purchase_record = Estimate_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).count()
            # total_today_sale = Estimate_Purchase.objects.filter(date=date.today()).aggregate(Sum('Total_amount'))
            totalpurchase = Estimate_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Total_amount'))
            purchase_round_off = Estimate_Purchase.objects.filter(date__day=day,date__month=month,date__year=year).aggregate(Sum('Round_off'))
            total_purchase = totalpurchase['Total_amount__sum']
            purchaseroundoff = purchase_round_off['Round_off__sum']
            if total_purchase_record == 0:
                print("Estimate Sale Total")
            elif today_purchase_record == 0:
                print("Estimate Today Sale")
            else:
                today_purchase = float(total_purchase) - float(purchaseroundoff)

            #Current Month Estimate Purchase
            total_purchase_record = Estimate_Purchase.objects.all().count()
            current_month_purchase = 0
            current_total_purchase = Estimate_Purchase.objects.filter(date__month=month,date__year=year).aggregate(Sum('Total_amount'))
            current_roundoff_purchase = Estimate_Purchase.objects.filter(date__month=month,date__year=year).aggregate(Sum('Round_off'))
            current_total_eatimate_purchase = current_total_purchase['Total_amount__sum']
            current_roundoff_estimate_purchase = current_roundoff_purchase['Round_off__sum']
            if total_purchase_record == 0:
                print("Current Month Estimate Purchase")
            elif today_purchase_record == 0:
                print("Current Month Estimate Purchase")
            else:
                current_month_purchase = float(current_total_eatimate_purchase) - float(current_roundoff_estimate_purchase)

            # Previous Month Estimate Purchase
            previous_month_total_purchase = 0
            previous_total_purchase_count = Estimate_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).count()
            if previous_total_purchase_count == 0:
                print("Previous Month Estimate Purchase")
            else:
                previous_purchase_total = Estimate_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Total_amount'))
                previous_purchase_roundoff = Estimate_Purchase.objects.filter(date__month=lastmonth,date__year=lastyear).aggregate(Sum('Round_off'))
                previous_total_purchase = previous_purchase_total['Total_amount__sum']
                previous_roundoff_purchase = previous_purchase_roundoff['Round_off__sum']
                previous_month_total_purchase = float(previous_total_purchase) - float(previous_roundoff_purchase)

            #Total Estimate Purchase
            Total_Eatimate_Purchase = 0
            if total_purchase_record == 0:
                print("Total Estimate Purchase")
            else:
                total_estimate_purchase = Estimate_Purchase.objects.all().aggregate(Sum('Total_amount'))
                roundoff_estimate_purchase = Estimate_Purchase.objects.all().aggregate(Sum('Round_off'))
                estimate_purchase = total_estimate_purchase['Total_amount__sum']
                estimate_roundoff = roundoff_estimate_purchase['Round_off__sum']
                Total_Eatimate_Purchase = float(estimate_purchase) - float(estimate_roundoff)

            #Stock
            # count = 0
            # productdata = Product.objects.all().count()
            # pcount = int(productdata)
            # print(pcount)

            # for i in range(1,pcount+1):
            #     Product_name = Product.objects.get(id=i).product_name
            #     Product_Minimum_Stock = Product.objects.get(id=i).minimum_stock
            #     Stock_Name = Stock.objects.get(id=i).product
            #     Stock_qty = Stock.objects.get(id=i).quantity

            #     if Stock_qty <= Product_Minimum_Stock:
            #         count += 1
            #         print(count)

            # outstock = count
            # instock = pcount - count
            # print(outstock)
            # print(instock)      

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
                # 'outstock':outstock,
                # 'instock':instock,
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
            return render(request,"pages/dashboard.html",context)
        if GST_group in user.groups.all():
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
            # total_today_sale = GST_Purchase.objects.filter(date=date.today()).aggregate(Sum('Total_amount'))
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

            #Stock
            # count = 0
            # productdata = Product.objects.all().count()
            # pcount = int(productdata)
            # print(pcount)

            # for i in range(1,pcount+1):
            #     Product_name = Product.objects.get(id=i).product_name
            #     Product_Minimum_Stock = Product.objects.get(id=i).minimum_stock
            #     Stock_Name = Stock.objects.get(id=i).product
            #     Stock_qty = Stock.objects.get(id=i).quantity

            #     if Stock_qty <= Product_Minimum_Stock:
            #         count += 1
            #         print(count)

            # outstock = count
            # instock = pcount - count
            # print(outstock)
            # print(instock)      

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
                # 'outstock':outstock,
                # 'instock':instock,
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
            return render(request,"pages/dashboard.html",context)
    else:
        return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('login')

def error404(request):
    return render(request,"pages/error404.html")

def user_name(request):
    user = User.objects.get(username=request.user.username)
    print(user)
    return user 