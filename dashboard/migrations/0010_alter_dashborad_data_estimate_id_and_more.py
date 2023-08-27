# Generated by Django 4.2.4 on 2023-08-27 04:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashborad_data_estimate',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='dashborad_data_estimate',
            name='model_name',
            field=models.CharField(default='Dashboard Estimate Data', max_length=50),
        ),
    ]
