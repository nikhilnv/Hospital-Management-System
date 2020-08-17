from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from . import models, forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
from django.conf import settings

# Create your views here.


def index(request):
    return render(request, 'index.html')


def specialities(request):
    return render(request, 'specialities.html')


def signup(request):
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            user.save()
            messages.success(request, 'You have been registered with us. You may sign in now')
            context = {
                'form': forms.SigninForm
            }
            return render(request, 'signin.html', context)
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        context = {
            'form': forms.SignupForm
        }
        return render(request, 'signup.html', context)


def signin(request):
    if request.method == 'POST':
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(request.user.username)
            user = User.objects.get(username=request.user.username)
            initial = {
                'username': request.user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            context = {
                'form': forms.UserDashboardForm(initial=initial)
            }
            return render(request, 'dashboard.html', context)
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect(signin)
    else:
        context = {
            'form': forms.SigninForm
        }
        return render(request, 'signin.html', context)


def contactus(request):
    if request.method == "POST":
        form = forms.ContactusForm(request.POST)
        if form.is_valid():
            contact = models.CustomerRelation(type_of_query=form.cleaned_data['type_of_query'],
                                              name=form.cleaned_data['name'],
                                              email=form.cleaned_data['email'],
                                              phone=form.cleaned_data['phone'],
                                              comments=form.cleaned_data['comments'])
            contact.save()
            messages.success(request, 'Your message has been sent. You will be contacted shortly.')
            context = {
                'form': forms.ContactusForm
            }
            return render(request, 'contactus.html', context)
        else:
            return render(request, 'contactus.html', {'form': form})
    else:
        context = {
                'form': forms.ContactusForm
            }
        return render(request, 'contactus.html', context)


def logout(request):
    auth.logout(request)
    context = {
        'form': forms.SigninForm
    }
    return render(request, 'signin.html', context)


@login_required(login_url="signin")
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    initial = {
        'username': request.user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    context = {
        'form': forms.UserDashboardForm(initial=initial)
    }
    return render(request, 'dashboard.html', context)


def deleteuser(request, uid):
    user = User.objects.get(id=uid)
    user.delete()
    messages.success(request, 'Your Account has been deleted successfully.')
    context = {
        'form': forms.SigninForm
    }
    return render(request, 'signin.html', context)


def updateuser(request, uid):
    form = forms.UserDashboardForm(request.POST)
    if form.is_valid():
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = User.objects.get(id=uid)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        messages.success(request, 'Your data has been updated successfully.')
        user = User.objects.get(username=request.user.username)
        initial = {
            'username': request.user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
         }
        context = {
            'form': forms.UserDashboardForm(initial=initial)
                }
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'dashboard.html', {'form': form})


@login_required(login_url="signin")
def scheduledetails(request):
    initial = {'username': request.user.username}
    context = {
        'form': forms.ScheduleDetailsForm(initial=initial)
    }
    return render(request, 'scheduledetails.html', context)


@login_required(login_url="signin")
def scheduledatetime(request):
    if request.method == 'POST':
        form = forms.ScheduleDetailsForm(request.POST)
        if form.is_valid():
            request.session['username'] = request.POST['username']
            request.session['patient_name'] = request.POST['patient_name']
            request.session['patient_gender'] = request.POST['gender']
            request.session['patient_age'] = request.POST['age']
            request.session['email'] = request.POST['email']
            request.session['phone'] = request.POST['phone']
            context = {
                'form': forms.ScheduleDateTimeForm()
            }
            return render(request, 'scheduledatetime.html', context)
        else:
            return render(request, 'scheduledetails.html', {'form': form})


@login_required(login_url="signin")
def scheduledoctor(request):
    if request.method == 'POST':
        form = forms.ScheduleDateTimeForm(request.POST)
        if form.is_valid():
            request.session['specialization'] = request.POST['speciality']
            request.session['booking_date'] = request.POST['date']
            request.session['booking_time'] = request.POST['time']
            request.session['booking_day'] = request.POST['day']
            doctors = models.Doctor.objects.filter(specialization=request.POST['speciality'])
            context = {
                'doctors': doctors
            }
            return render(request, 'scheduledoctor.html', context)
        else:
            print(form.errors)
            context = {
                'form': forms.ScheduleDateTimeForm()
            }
            return render(request, 'scheduledatetime.html', context)
    else:
        doctors = models.Doctor.objects.filter(specialization=request.session.get('specialization'))
        context = {
            'doctors': doctors
        }
        return render(request, 'scheduledoctor.html', context)


@login_required(login_url="signin")
def bookappointment(request):
    if request.method == 'POST':
        request.session['doctor_name'] = request.POST['doctorname']
        request.session['appointment_price'] = request.POST['pay_per_appointment']
        initial = {'username': request.session.get('username'),
                   'patient_name': request.session.get('patient_name'),
                   'patient_age': request.session.get('patient_age'),
                   'patient_gender': request.session.get('patient_gender'),
                   'email': request.session.get('email'),
                   'phone': request.session.get('phone'),
                   'booking_date': request.session.get('booking_date'),
                   'booking_time': request.session.get('booking_time'),
                   'day': request.session.get('booking_day'),
                   'doctor_name': request.session.get('doctor_name'),
                   'specialization': request.session.get('specialization'),
                   'appointment_price': request.session.get('appointment_price')
                   }
        context = {
            'form': forms.BookAppointmentForm(initial=initial)
        }
        return render(request, 'bookappointment.html', context)
    else:
        doctors = models.Doctor.objects.filter(specialization=request.session.get('speciality'))
        context = {
            'doctors': doctors
            }
        return render(request, 'scheduledoctor.html', context)


@login_required(login_url="signin")
def bookappointment_done(request, paid):
    if request.method == "POST":
        form = forms.BookAppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = models.Appointment(username=form.cleaned_data['username'],
                                                 patient_name=form.cleaned_data['patient_name'],
                                                 age=form.cleaned_data['patient_age'],
                                                 gender=form.cleaned_data['patient_gender'],
                                                 email=form.cleaned_data['email'],
                                                 phone=form.cleaned_data['phone'],
                                                 booking_date=form.cleaned_data['booking_date'],
                                                 booking_time=form.cleaned_data['booking_time'],
                                                 booking_day=form.cleaned_data['day'],
                                                 doctor_name=form.cleaned_data['doctor_name'],
                                                 specialization=form.cleaned_data['specialization'],
                                                 appointment_price=form.cleaned_data['appointment_price'],
                                                 paid=paid)
            new_appointment.save()
            send_mail(
                'Appointment Booked',     # SUBJECT
                'Appointment of ' + request.POST['patient_name'] + ' has been booked with ' + request.POST['doctor_name']
                + ' for ' + request.POST['specialization'] + ' on ' + request.POST['booking_date'] + ' at ' +
                request.POST['booking_time'],      # MESSAGE
                'Medicarehospital91@gmail.com',  # FROM EMAIL ID
                [request.POST['email']],  # TO EMAIL ID
                fail_silently=False,
            )
            appointments = models.Appointment.objects.filter(username=request.user.username)
            context = {
                'appointments': appointments
            }
            return render(request, 'myappointment.html', context)
    else:
        initial = {'username': request.session.get('username'),
                   'patient_name': request.session.get('patient_name'),
                   'patient_age': request.session.get('patient_age'),
                   'patient_gender': request.session.get('patient_gender'),
                   'email': request.session.get('email'),
                   'phone': request.session.get('phone'),
                   'booking_date': request.session.get('booking_date'),
                   'booking_time': request.session.get('booking_time'),
                   'day': request.session.get('booking_day'),
                   'doctor_name': request.session.get('doctor_name'),
                   'specialization': request.session.get('specialization'),
                   'appointment_price': request.session.get('appointment_price')
                   }
        context = {
            'form': forms.BookAppointmentForm(initial=initial)
        }
        return render(request, 'bookappointment.html', context)


@login_required(login_url="signin")
def bookappointment_pay(request, paid):
    if request.method == "POST":
        form = forms.BookAppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = models.Appointment(username=form.cleaned_data['username'],
                                                 patient_name=form.cleaned_data['patient_name'],
                                                 age=form.cleaned_data['patient_age'],
                                                 gender=form.cleaned_data['patient_gender'],
                                                 email=form.cleaned_data['email'],
                                                 phone=form.cleaned_data['phone'],
                                                 booking_date=form.cleaned_data['booking_date'],
                                                 booking_time=form.cleaned_data['booking_time'],
                                                 booking_day=form.cleaned_data['day'],
                                                 doctor_name=form.cleaned_data['doctor_name'],
                                                 specialization=form.cleaned_data['specialization'],
                                                 appointment_price=form.cleaned_data['appointment_price'],
                                                 paid=paid,
                                                 order_id=Checksum.__id_generator__())
            new_appointment.save()
            data_dict = {

                'MID': settings.PAYTM_MERCHANT_ID,
                'ORDER_ID': str(new_appointment.order_id),
                'TXN_AMOUNT': str(new_appointment.appointment_price),
                'CUST_ID': new_appointment.email,
                'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
                'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,

                }
            data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
            return render(request, 'paytm.html', {'data_dict': data_dict})
                    

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, settings.PAYTM_MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            data = models.Appointment.objects.get(order_id=response_dict['ORDERID'])
            send_mail(
                'Appointment Booked',     # SUBJECT
                'Appointment of ' + data.patient_name + ' has been booked with ' + data.doctor_name
                + ' for ' + data.specialization + ' on ' + data.booking_date + ' at ' +
                data.booking_time,      # MESSAGE
                'Medicarehospital91@gmail.com',  # FROM EMAIL ID
                [data.email],  # TO EMAIL ID
                fail_silently=False,
            )
            return redirect(myappointment)
        else:
            models.Appointment.objects.filter(order_id=response_dict['ORDERID']).delete()
            messages.error(request, "Payment was not successful as " + response_dict['RESPMSG'])
            return redirect(bookappointment_done, paid="No")


@login_required(login_url="signin")
def myappointment(request):
    appointments = models.Appointment.objects.filter(username=request.user.username)
    context = {
        'appointments': appointments
    }
    return render(request, 'myappointment.html', context)
