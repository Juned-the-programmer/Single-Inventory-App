from django.db import models
from django.db.models.signals import post_save
import uuid

# Create your models here.
class dashborad_data_estimate(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    model_name = models.CharField(default="Dashboard Estimate Data", max_length=50)

    today_estimate_sale = models.FloatField(null=True, blank=True, default=0)
    total_estimate_sale = models.FloatField(null=True, blank=True, default=0)
    current_month_estimate_sale = models.FloatField(null=True, blank=True, default=0)
    previous_month_estimate_sale = models.FloatField(null=True, blank=True, default=0)

    today_estimate_purchase = models.FloatField(null=True, blank=True, default=0)
    total_estimate_purchase = models.FloatField(null=True, blank=True, default=0)
    current_month_estimate_purchase = models.FloatField(null=True, blank=True, default=0)
    previous_month_estimate_purchase = models.FloatField(null=True, blank=True, default=0)

    current_month_profit = models.FloatField(null=True, blank=True, default=0)
    previous_month_profit = models.FloatField(null=True, blank=True, default=0)
    total_profit = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.model_name

    @property
    def current_month_profit(self):
        return self.current_month_estimate_sale - self.current_month_estimate_purchase

    @property
    def previous_month_profit(self):
        return self.previous_month_estimate_sale - self.previous_month_estimate_purchase

    @property
    def total_profit(self):
        return self.total_estimate_sale - self.total_estimate_purchase