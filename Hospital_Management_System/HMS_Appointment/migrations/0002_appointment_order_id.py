# Generated by Django 3.1 on 2020-08-15 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HMS_Appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]