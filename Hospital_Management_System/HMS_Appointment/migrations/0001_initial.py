# Generated by Django 3.0.7 on 2020-07-01 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('patient_name', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phone', models.BigIntegerField()),
                ('booking_date', models.DateField()),
                ('booking_time', models.TimeField()),
                ('booking_day', models.CharField(max_length=30)),
                ('doctor_name', models.CharField(max_length=50)),
                ('specialization', models.CharField(max_length=50)),
                ('appointment_price', models.IntegerField()),
                ('paid', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_query', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phone', models.BigIntegerField()),
                ('comments', models.TextField(max_length=2083)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('specialization', models.CharField(max_length=30)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phone', models.BigIntegerField()),
                ('address', models.CharField(max_length=100)),
                ('pay_per_appointment', models.IntegerField(default=300)),
            ],
        ),
    ]
