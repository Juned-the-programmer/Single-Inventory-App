# Generated by Django 3.2.5 on 2023-08-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_estimate',
            name='supplier_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='supplier_gst',
            name='supplierid',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
