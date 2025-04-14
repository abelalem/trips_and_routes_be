# Generated by Django 5.1.7 on 2025-04-12 07:52

import driver_logs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_logs', '0009_driverlog_truck_info_delete_truck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverlog',
            name='truck_info',
            field=models.JSONField(default=driver_logs.models.DriverLog.truck_info_default, verbose_name='TruckInfo'),
        ),
    ]
