from django.db import models
import uuid

# Create your models here.
class dailyincome_estimate(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.name

class dailyincome_gst(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.name

class dailyexpense_estimate(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category

class dailyexpense_gst(models.Model):
    category =models.CharField(max_length=50)
    amount = models.FloatField()
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category

class category_estimate(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category_name

class category_gst(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)

    def __str__(self):
        return self.category_name