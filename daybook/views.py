from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *


# Create your views here.
@login_required(login_url='login')
def dailyincome(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')   
    user = User.objects.get(username=request.user.username)

    if user.is_authenticated:
        if request.method == 'POST':
            if 'Estimate' in request.POST:

                DailyIncome = dailyincome_estimate(
                    name=request.POST['name'],
                    amount=request.POST['amount']
                )
                DailyIncome.save()
                messages.success(request,"Daily Income Added Successfully !")
            else:
                DailyIncome = dailyincome_gst(
                    name = request.POST['name'],
                    amount=request.POST['amount']
                )
                DailyIncome.save()
                messages.success(request,"Daily DailyIncome Successfully ! ")
        
        date_ = date.today()
        d1 = date_.strftime("%d/%m/%Y")
        d2 = date_.strftime("%Y-%m-%d")

        if Estimate_group in user.groups.all():
            Dailyincome_data = dailyincome_estimate.objects.filter(date=d2)

        if GST_group in user.groups.all():
            Dailyincome_data = dailyincome_gst.objects.filter(date=d2)

        context = {
            'd1':d1,
            'Dailyincome_data' : Dailyincome_data
        }
        return render(request, 'daybook/dailyincome.html',context)
    else:
        return redirect('login')
    
@login_required(login_url='login')
def dailyexpense(request):
    Estimate_group = Group.objects.get(name='Estimate')
    GST_group = Group.objects.get(name='GST')
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            if request.method == 'POST':
                if 'GST' in request.POST:
                    DailyExpense = dailyexpense_gst(
                        category=request.POST['category'],
                        amount=request.POST['amount'],
                        name=request.POST['name']
                    )
                    DailyExpense.save()

                elif 'addcategory_gst' in request.POST:
                    Category = category_gst(
                        category_name=request.POST['cat'],
                    )
                    Category.save()

                elif 'Estimate' in request.POST:
                    DailyExpense = dailyexpense_estimate(
                        category=request.POST['category'],
                        amount=request.POST['amount'],
                        name=request.POST['name']
                    )
                    DailyExpense.save()

                else:
                    Category = category_estimate(
                        category_name=request.POST['cat'],
                    )
                    Category.save()
            
            date_ = date.today()
            d1 = date_.strftime("%d/%m/%Y")
            d2 = date_.strftime("%Y-%m-%d")

            if Estimate_group in user.groups.all():
                DailyExpense_data = dailyexpense_estimate.objects.filter(date=d2)
                category_data = category_estimate.objects.all()

            if GST_group in user.groups.all():
                DailyExpense_data = dailyexpense_gst.objects.filter(date=d2)
                category_data = category_gst.objects.all()

            context = {
                'd1':d1,
                'DailyExpense_data' : DailyExpense_data,
                'category_data' : category_data
            }
            return render(request , 'daybook/dailyexpense.html',context)
        else:
            return redirect('login')
    except:
        return redirect('error404')