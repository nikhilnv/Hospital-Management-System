from django.contrib import admin
from . import models
# Register your models here.


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('username', 'patient_name', 'phone', 'doctor_name', 'specialization', 'booking_date', 'booking_time',
                    'appointment_price', 'paid')

class CustomerRelationAdmin(admin.ModelAdmin):
    list_display = ('type_of_query', 'name', 'email', 'comments') 

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'phone', 'address', 'pay_per_appointment')

admin.site.register(models.CustomerRelation, CustomerRelationAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
