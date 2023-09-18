from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *

# To add the daily Income some extra Income which is not going to add into the sell.
@login_required(login_url='login')
def dailyincome(request):
    if request.method == 'POST':
        # Check for User Groups 
        if request.session['Estimate']:

            DailyIncome = dailyincome_estimate(
                name=request.POST['name'],
                amount=request.POST['amount']
            )
            # save
            DailyIncome.save()
            messages.success(request,"Daily Income Added Successfully !")

        # Check for User Groups 
        if request.session['GST']:
            DailyIncome = dailyincome_gst(
                name = request.POST['name'],
                amount=request.POST['amount']
            )
            # save
            DailyIncome.save()
            messages.success(request,"Daily DailyIncome Successfully ! ")
    
    # Get the date
    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")
    d2 = date_.strftime("%Y-%m-%d")

    # Check for user Group
    if request.session['Estimate']:
        # Get today's Income data 
        Dailyincome_data = dailyincome_estimate.objects.filter(date=d2)

    # Check for user Group
    if request.session['GST']:
        Dailyincome_data = dailyincome_gst.objects.filter(date=d2)

    context = {
        'd1':d1,
        'Dailyincome_data' : Dailyincome_data
    }
    return render(request, 'daybook/dailyincome.html',context)
    
# To add the daily Expense it can be anything like petrol, food, stay anything. But to add this we need to add category also.
@login_required(login_url='login')
def dailyexpense(request):
    if request.method == 'POST':
        # Check for user Group
        if request.session['Estimate']:
            if 'Estimate' in request.POST:
                DailyExpense = dailyexpense_estimate(
                        category=request.POST['category'],
                        amount=request.POST['amount'],
                        name=request.POST['name']
                )
                # save
                DailyExpense.save()
            else:
                # Add category
                Category = category_estimate(category_name=request.POST['cat'])
                Category.save()
        
        # check for user Group
        if request.session['GST']:
            if 'GST' in request.POST:
                DailyExpense = dailyexpense_gst(
                    category=request.POST['category'],
                    amount=request.POST['amount'],
                    name=request.POST['name']
                )
                # save
                DailyExpense.save()
            else:
                # Add category
                Category = category_estimate(category_name=request.POST['cat'])
                Category.save()
            
    
    date_ = date.today()
    d1 = date_.strftime("%d/%m/%Y")
    d2 = date_.strftime("%Y-%m-%d")

    # Check for User Group
    if request.session['Estimate']:
        # Get today's expense data
        DailyExpense_data = dailyexpense_estimate.objects.filter(date=d2)
        # Get total category data
        category_data = category_estimate.objects.all()
    
    # Check for User Group
    if request.session['GST']:
        # Get today's expense data
        DailyExpense_data = dailyexpense_gst.objects.filter(date=d2)
        # Get total category data
        category_data = category_gst.objects.all()

    context = {
        'd1':d1,
        'DailyExpense_data' : DailyExpense_data,
        'category_data' : category_data
    }
    return render(request , 'daybook/dailyexpense.html',context)