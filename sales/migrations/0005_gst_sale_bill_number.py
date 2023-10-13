# Generated by Django 4.2.4 on 2023-10-09 18:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_rename_bill_number_estimate_sale_bill_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='GST_sale_bill_number',
            fields=[
                ('last_bill_number', models.IntegerField()),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]