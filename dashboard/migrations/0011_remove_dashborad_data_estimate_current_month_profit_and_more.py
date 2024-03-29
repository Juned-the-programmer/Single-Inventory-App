# Generated by Django 4.2.4 on 2023-08-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_dashborad_data_estimate_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashborad_data_estimate',
            name='current_month_profit',
        ),
        migrations.RemoveField(
            model_name='dashborad_data_estimate',
            name='previous_month_profit',
        ),
        migrations.RemoveField(
            model_name='dashborad_data_estimate',
            name='total_profit',
        ),
        migrations.AddField(
            model_name='dashborad_data_estimate',
            name='total_customer_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='dashborad_data_estimate',
            name='total_product_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='dashborad_data_estimate',
            name='total_supplier_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
