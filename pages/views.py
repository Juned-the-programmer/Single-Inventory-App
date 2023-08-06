import datetime
import os
import zipfile
from datetime import date
import tablib

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, auth
from django.core.files.storage import default_storage
from django.db.models import Avg, Max, Min, Sum
from django.shortcuts import HttpResponse, redirect, render
from import_export import fields, resources, results, widgets
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

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

def export_backup(request):
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="backup.zip"'

    # Get all installed apps in the project
    installed_apps = apps.get_app_configs()

    with zipfile.ZipFile(response, 'w') as zip_file:
        for app in installed_apps:
            # Get all models for each app
            models = app.get_models()

            for model in models:
                # Define a resource class for each model dynamically
                class_name = f"{model.__name__}Resource"
                ModelResource = type(class_name, (resources.ModelResource,), {'Meta': type('Meta', (), {'model': model})})

                # Export the model's data to CSV and add it to the ZIP file
                queryset = model.objects.all()
                model_resource = ModelResource()
                dataset = model_resource.export(queryset)
                zip_file.writestr(f'{app.label}_{model.__name__}.csv', dataset.csv)

    return response

def backup_page(request):
    return render(request, 'pages/backup.html')

def import_backup(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']

        # Save the uploaded file to a temporary location
        file_path = default_storage.save(backup_file.name, backup_file)

        # Extract the ZIP file and read the CSVs
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            for filename in zip_file.namelist():
                with zip_file.open(filename) as csv_file:
                    # Identify the model based on the filename
                    app_label, model_name = os.path.splitext(filename)[0].split('_', 1)
                    model = apps.get_model(app_label, model_name)

                    # Define a resource class for each model dynamically
                    class_name = f"{model.__name__}Resource"
                    ModelResource = type(class_name, (resources.ModelResource,), {'Meta': type('Meta', (), {'model': model})})

                    # Read the CSV data and create a dataset
                    dataset = tablib.Dataset().load(csv_file.read().decode())

                    # Import data from the dataset to the model
                    model_resource = ModelResource()
                    result = model_resource.import_data(dataset, dry_run=False)

        # Delete the temporary file
        os.remove(file_path)
        
    return render(request, 'pages/restore.html')