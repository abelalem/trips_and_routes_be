# Generated by Django 5.1.7 on 2025-04-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20250331_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='login_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
