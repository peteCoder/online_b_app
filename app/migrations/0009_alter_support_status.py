# Generated by Django 4.2.9 on 2024-10-26 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_support_status_alter_support_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Fulfilled', 'Fulfilled')], max_length=400, null=True),
        ),
    ]
