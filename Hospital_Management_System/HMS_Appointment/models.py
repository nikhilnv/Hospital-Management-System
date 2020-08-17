from django.db import models

# Create your models here.


class CustomerRelation(models.Model):
    type_of_query = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    email = models.EmailField(default=None)
    phone = models.BigIntegerField()
    comments = models.TextField(max_length=2083)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=40)
    specialization = models.CharField(max_length=30)
    email = models.EmailField(default=None)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    pay_per_appointment = models.IntegerField(default=300)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    username = models.CharField(max_length=40)
    patient_name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    email = models.EmailField(default=None)
    phone = models.BigIntegerField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    booking_day = models.CharField(max_length=30)
    doctor_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)
    appointment_price = models.IntegerField()
    paid = models.CharField(max_length=5)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
