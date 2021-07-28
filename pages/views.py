from django.shortcuts import render , redirect
from django.contrib.auth.models import auth,User,Group
from django.contrib import messages
from .models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True)
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
    user = User.objects.get(username=request.user.username)
    try:
        if user.is_authenticated:
            return render(request,"pages/dashboard.html")
        else:
            return redirect('login')
    except:
        return redirect('error404')
        messages.error(request, "Something went wrong")

def logout(request):
    auth.logout(request)
    return redirect('login')

def error404(request):
    return render(request,"pages/error404.html")