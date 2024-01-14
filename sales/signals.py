from django.db.models.signals import post_save
from .models import *
from dashboard.models import dashborad_data_estimate
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=Estimate_sales)
def update_estiamte_dashboard_data(sender, instance, created, **kwargs):
    dashborad_data = dashborad_data_estimate.objects.get(model_name="Dashboard Estimate Data")
    today =timezone.now().date()

    if created:
        # Total Estimate Sale
        dashborad_data.total_estimate_sale += float(instance.Total_amount)

        # Today Estimate Sale
        if instance.date == today:
            dashborad_data.today_estimate_sale += float(instance.Total_amount)

        # Current Month Estimate Sale
        if instance.date.month == today.month and instance.date.year == today.year:
            dashborad_data.current_month_estimate_sale += float(instance.Total_amount)

        dashborad_data.save()