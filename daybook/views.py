from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *

# Create your views here.
@login_required(login_url='login')
def dailyincome(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():

            DailyIncome = dailyincome_estimate(
                name=request.POST['name'],
                amount=request.POST['amount']
            )
            DailyIncome.save()
            messages.success(request,"Daily Income Added Successfully !")
        
        if request.user.groups.filter(name='GST').exists():
            DailyIncome = dailyincome_gst(
                name = request.POST['name'],
                amount=request.POST['amount']
            )
            DailyIncome.save()
            messages.success(request,"Daily DailyIncome Successfully ! ")
    
    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")
    d2 = date_.strftime("%Y-%m-%d")

    if request.user.groups.filter(name='Estimate').exists():
        Dailyincome_data = dailyincome_estimate.objects.filter(date=d2)

    if request.user.groups.filter(name='GST').exists():
        Dailyincome_data = dailyincome_gst.objects.filter(date=d2)

    context = {
        'd1':d1,
        'Dailyincome_data' : Dailyincome_data
    }
    return render(request, 'daybook/dailyincome.html',context)
    
@login_required(login_url='login')
def dailyexpense(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Estimate').exists():
            if 'addcategory_estimate' in request.POST:
                Category = category_gst(
                    category_name=request.POST['cat'],
                )
                Category.save()
            else:
                DailyExpense = dailyexpense_gst(
                    category=request.POST['category'],
                    amount=request.POST['amount'],
                    name=request.POST['name']
                )
                DailyExpense.save()

        if request.user.groups.filter(name='GST').exists():
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

    if request.user.groups.filter(name='Estimate').exists():
        DailyExpense_data = dailyexpense_estimate.objects.filter(date=d2)
        category_data = category_estimate.objects.all()

    if request.user.groups.filter(name='GST').exists():
        DailyExpense_data = dailyexpense_gst.objects.filter(date=d2)
        category_data = category_gst.objects.all()

    context = {
        'd1':d1,
        'DailyExpense_data' : DailyExpense_data,
        'category_data' : category_data
    }
    return render(request , 'daybook/dailyexpense.html',context)