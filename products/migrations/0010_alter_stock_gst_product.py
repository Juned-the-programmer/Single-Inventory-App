# Generated by Django 4.2.4 on 2023-10-08 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_required_to_manufacture_gst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_gst',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock_gst', to='products.product_gst'),
        ),
    ]