from celery.task import periodic_task
from datetime import time, timedelta
from dashboard.models import dashborad_data_estimate
from datetime import datetime
from celery import shared_task
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from celery.schedules import crontab

# Added Shared Task which we can use at multiple places.
''' Usage : 
    This is used to reset the values for the previous and current month sale and purchase data.
    It will replace the value of current month sale and purchase data to previous month sale and purchase data.
    And for the current month it will reset the value again to 0.
'''
@shared_task
def reset_monthly_estimates():
    today = datetime.today()
    current_month_start = today.replace(day=1)
    previous_month_start = current_month_start - relativedelta(months=1)

    dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
    
    # Update previous_month_estimate_purchase with current_month_estimate_purchase
    dashboard_data.previous_month_estimate_purchase = dashboard_data.current_month_estimate_purchase

    # update previous_month_estiamte_sale with current_month_estimate_sale
    dashboard_data.previous_month_estimate_sale = dashboard_data.current_month_estimate_sale

    # Reset current_month_estimate_purchase and current_month_estimate_sale to 0
    dashboard_data.current_month_estimate_purchase = 0
    dashboard_data.current_month_estimate_sale = 0
    
    dashboard_data.save()

# Periodic Task for reseting estimate sale and Purchase.
''' Usage : 
    This will run every day to reset the value of today_estimate_purchase and today_estimate_sale. As this 2 data we are using in dashboard to populate the value. 
    Check the dashboard.models file to see the model for dashboard.
'''
@periodic_task(run_every=timedelta(days=1), time=time(hour=0, minute=0, second=0))
def reset_today_estimate():
    dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
    dashboard_data.today_estimate_purchase = 0
    dashboard_data.today_estimate_sale = 0
    dashboard_data.save()

# Periodic task to to run on every last day of month at midnight.
@periodic_task(run_every=crontab(day_of_month='last'))
def reset_monthly_estimates_task():
    reset_monthly_estimates.delay()