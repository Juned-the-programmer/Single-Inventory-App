# Generated by Django 3.2.5 on 2022-05-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_customer_estimate_cusotmer_id'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='customer_estimate',
            name='dashboard_c_id_b45204_idx',
        ),
        migrations.RenameField(
            model_name='customer_estimate',
            old_name='first_name',
            new_name='contactno',
        ),
        migrations.RenameField(
            model_name='customer_estimate',
            old_name='cusotmer_id',
            new_name='customerid',
        ),
        migrations.RemoveField(
            model_name='customer_estimate',
            name='contact_no',
        ),
        migrations.RemoveField(
            model_name='customer_estimate',
            name='last_name',
        ),
        migrations.AddField(
            model_name='customer_estimate',
            name='fullname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
