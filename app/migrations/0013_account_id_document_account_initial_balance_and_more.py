# Generated by Django 4.2.9 on 2024-10-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_account_account_opening_date_account_interest_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='id_document',
            field=models.ImageField(blank=True, null=True, upload_to='id-document/'),
        ),
        migrations.AddField(
            model_name='account',
            name='initial_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='initial_deposit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='investment_history',
            field=models.ImageField(blank=True, null=True, upload_to='investment-history/'),
        ),
        migrations.AddField(
            model_name='account',
            name='penalty_for_early_withdrawal',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='account',
            name='proof_of_income',
            field=models.ImageField(blank=True, null=True, upload_to='proof-of-income/'),
        ),
        migrations.AddField(
            model_name='account',
            name='term_length',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='account',
            name='transaction_limit',
            field=models.IntegerField(default=100),
        ),
    ]