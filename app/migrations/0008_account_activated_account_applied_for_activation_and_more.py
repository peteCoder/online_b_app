# Generated by Django 4.2.9 on 2024-10-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_card_confirmation_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='applied_for_activation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='confirmation_receipt',
            field=models.ImageField(blank=True, null=True, upload_to='receipts/'),
        ),
        migrations.AddField(
            model_name='account',
            name='deposit_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings'), ('OTHER', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='account',
            name='ach_routing',
            field=models.CharField(blank=True, default='2171 SE Federal Highway Stuart, Florida 34994', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='location',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]