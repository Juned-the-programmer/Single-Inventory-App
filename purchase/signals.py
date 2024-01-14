from django.db.models.signals import post_save
from .models import *
from dashboard.models import dashborad_data_estimate
from django.dispatch import receiver
from django.utils import timezone

''' We are using this signals to update the dashboard data when we will save the purchase record. 
Here we are upading 3 values from that named as a Total, Today and Current month Estimate purchase'''
@receiver(post_save, sender=Estimate_Purchase)
def update_estimate_dashboard_data(sender, instance, created, **kwargs):
    dashboard_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
    today = timezone.now().date()
    if created:
        # Total Estimate Purchase
        dashboard_data.total_estimate_purchase += float(instance.Total_amount)

        # Today Estimate Purchase
        if instance.date == today:
            dashboard_data.today_estimate_purchase += float(instance.Total_amount)

        # Current Month Purchase
        if instance.date.month == today.month and instance.date.year == today.year:
            dashboard_data.current_month_estimate_purchase += float(instance.Total_amount)

        dashboard_data.save()