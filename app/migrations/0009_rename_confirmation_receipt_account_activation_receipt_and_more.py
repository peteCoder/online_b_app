# Generated by Django 4.2.9 on 2024-10-22 10:15

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_account_activated_account_applied_for_activation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='confirmation_receipt',
            new_name='activation_receipt',
        ),
        migrations.RemoveField(
            model_name='account',
            name='deposit_amount',
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(default=app.models.generate_account_number, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='ach_routing',
            field=models.CharField(blank=True, default=app.models.generate_ach_routing, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='location',
            field=models.CharField(blank=True, default=app.models.change_account_location, max_length=500, null=True),
        ),
    ]
