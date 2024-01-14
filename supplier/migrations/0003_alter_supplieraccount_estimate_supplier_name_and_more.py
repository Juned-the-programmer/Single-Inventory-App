# Generated by Django 4.2.4 on 2023-09-18 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20230802_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplieraccount_estimate',
            name='supplier_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier_estimate'),
        ),
        migrations.AlterField(
            model_name='supplieraccount_gst',
            name='supplier_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier_gst'),
        ),
    ]
