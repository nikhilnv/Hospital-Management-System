import string, re
from django import forms
from . import models
from datetime import timedelta
import datetime
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.models import User


class SigninForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'UserName',
        'id': 'inputUsername',
        'autocomplete': 'off'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'inputPassword'
    }))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'id': 'inputFirst_Name',
        'autocomplete': 'off'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'id': 'inputLast_Name',
        'autocomplete': 'off'
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'UserName',
        'id': 'inputUsername',
        'autocomplete': 'off'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'inputEmail',
        'autocomplete': 'off'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'inputPassword'
    }))

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name is not valid.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name is not valid.")
        return last_name

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password should be of atleast 8 characters.")
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with email address already exists.")
        return email


class ContactusForm(forms.Form):
    CHOICES = [('enquiry', 'Enquiry'),
               ('compliment', 'Compliment'),
               ('complaint', 'Complaint'),
               ('others', 'Others')]
    type_of_query = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    }))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
        'id': 'inputName',
        'autocomplete': 'off'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'inputEmail',
        'autocomplete': 'off'
    }))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone',
        'id': 'inputPhone'
    }))
    comments = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Please write your query',
        'id': 'inputComments',
        'rows': 5,
        'cols': 40
    }))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError("Name is not valid.")
        return name

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone'))
        if not re.match(r'[789]\d{9}$', phone):
            raise forms.ValidationError("Invalid Phone Number")
        return phone


class UserDashboardForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'inputUsername',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'id': 'inputFirst_Name',
        'autocomplete': 'off'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
        'id': 'inputLast_Name',
        'autocomplete': 'off'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'inputEmail',
        'autocomplete': 'off'
    }))

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name is not valid.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name is not valid.")
        return last_name


class ScheduleDetailsForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'inputUsername',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    patient_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Patient Name',
        'id': 'inputPatientName',
        'autocomplete': 'off'
    }))
    CHOICES = [('male', 'Male'),
               ('female', 'Female'),
               ('others', 'Others')]
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input',
        'id': 'inputGender'
    }))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Age',
        'id': 'inputAge'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'inputEmail',
        'autocomplete': 'off'
    }))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'inputPhone',
        'placeholder': 'Phone',
        'autocomplete': 'off'
       }))

    def clean_patient_name(self):
        patient_name = self.cleaned_data.get('patient_name')
        if not patient_name.isalpha():
            raise forms.ValidationError("Name is not valid.")
        return patient_name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not (1 <= age <= 120):
            raise forms.ValidationError("Invalid age")
        return age

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone'))
        if not re.match(r'[789]\d{9}$', phone):
            raise forms.ValidationError("Invalid Phone Number")
        return phone


class ScheduleDateTimeForm(forms.Form):
    speciality = forms.ModelChoiceField(queryset=models.Doctor.objects.all().values_list
     ("specialization", flat=True).distinct(), to_field_name='specialization',
             empty_label="-----Select Speciality-----", widget=forms.Select(attrs={
                      'class': 'form-control',
                      'id': 'inputSpeciality'
    }))
    date = forms.DateField(input_formats=['%Y-%m-%d'],  widget=DatePickerInput(attrs={
        'id': 'datepicker', 'onblur': 'getWeekDay();'}, format='%Y-%m-%d', options={
        'minDate': str(datetime.date.today() + timedelta(days=1))
    }))
    time = forms.TimeField(widget=TimePickerInput(attrs={'id': 'timepicker', 'onblur': 'getTime()'}, options={
        'stepping': 15,
        "showTodayButton": False
    }))
    day = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputDay',
        'readonly': 'readonly'
    }))


class BookAppointmentForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputUsername',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    patient_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputPatientName',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    patient_gender = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputPatientGender',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    patient_age = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'inputAge',
        'readonly': 'readonly'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'inputEmail',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'inputPhone',
        'readonly': 'readonly'
    }))
    booking_date = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputBooking_date',
        'readonly': 'readonly'
    }))
    booking_time = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputBooking_time',
        'readonly': 'readonly'
    }))
    day = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputDay',
        'readonly': 'readonly'
    }))
    doctor_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputDoctor_name',
        'readonly': 'readonly'
    }))
    specialization = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputSpecialization',
        'readonly': 'readonly'
    }))
    appointment_price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'inputAppointment_price',
        'readonly': 'readonly'
    }))