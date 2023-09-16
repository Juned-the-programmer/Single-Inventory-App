# Generated by Django 4.2.4 on 2023-09-15 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_required_to_manufacture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_required_to_manufacture',
            name='manufacture_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufactured_products', to='products.product_estimate'),
        ),
        migrations.AlterField(
            model_name='product_required_to_manufacture',
            name='required_products',
            field=models.ManyToManyField(blank=True, related_name='required_products_for_manufacture', to='products.product_required_to_manufacture'),
        ),
    ]
