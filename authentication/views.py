from django.contrib import messages
from django.contrib.auth.models import Group, User, auth
from django.shortcuts import redirect, render

from .models import *


# Create your views here.
def login(request):
    if request.method == 'POST':   
        user_login = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user_login is not None:
            auth.login(request,user_login)
            messages.success(request,"Login Successfull")

            request.session['company_name'] = user_login.profile.company_name
            request.session['username'] = user_login.username
            request.session['ownerstate'] = user_login.profile.state

            if user_login.groups.filter(name="Estimate").exists():
                request.session['Estimate'] = True
            else:
                request.session['Estimate'] = False

            if user_login.groups.filter(name="GST").exists():
                request.session['GST'] = True
            else:
                request.session['GST'] = False
            
            if user_login.groups.filter(name="Manufacture").exists():
                request.session['Manufacture'] = True
            else:
                request.session['Manufacture'] = False

            return redirect('dashboard')
        else:
            print("Login Again")
            messages.error(request , "Invalid Username or Password")

    return render(request,"authentication/login.html")

def signup_gst(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordrepeat']:
            user_signup = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
            user_signup.save()

            add_group = Group.objects.get_or_create(name='GST')
            add_group = Group.objects.get_or_create(name='Estimate')
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

    return render(request,"authentication/signup_gst.html")

def signup_estimate(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordrepeat']:
            user_signup = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
            user_signup.save()
            
            add_group = Group.objects.get_or_create(name='GST')
            add_group = Group.objects.get_or_create(name='Estimate')
            add_group = Group.objects.get(name='Estimate')
            add_group.user_set.add(user_signup)

            user_login = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
            if user_login is not None:
                auth.login(request,user_login)
                if user_login.groups.filter(name="Estimate").exists():
                    request.session['Estimate'] = True
                else:
                    request.session['Estimate'] = False

                if user_login.groups.filter(name="GST").exists():
                    request.session['GST'] = True
                else:
                    request.session['GST'] = False
                
                if user_login.groups.filter(name="Manufacture").exists():
                    request.session['Manufacture'] = True
                else:
                    request.session['Manufacture'] = False
            else:
                print("Singup Again")
            
            if request.POST['Manufacture'] == "Yes":
                add_group = Group.objects.get_or_create(name="Manufacture")
                add_group = Group.objects.get(name='Manufacture')
                add_group.user_set.add(user_signup)

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
    return render(request,"authentication/signup-estimate.html")

def logout(request):
    auth.logout(request)
    return redirect('login')