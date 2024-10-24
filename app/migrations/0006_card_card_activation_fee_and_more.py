# Generated by Django 4.2.9 on 2024-10-21 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_card_applied_for_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_activation_fee',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='card',
            name='applied_for_activation',
            field=models.BooleanField(default=False),
        ),
    ]
