import datetime
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, auth
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import HttpResponse, redirect, render

from dashboard.models import *
from products.models import *
from purchase.models import *
from sales.models import *

from .models import *

# Create your views here.

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

def error404(request):
    return render(request,"pages/error404.html")

def user_name(request):
    user = User.objects.get(username=request.user.username)
    print(user)
    return user 