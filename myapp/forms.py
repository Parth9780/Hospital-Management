from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = '__all__'

class LoginForm(forms.ModelForm):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'time', 'department', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name', 'email', 'message']

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['username','email','password']

class forpass(forms.ModelForm):
    class Meta:
        model=Register
        fields=['password']

class updateAppointment(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'time', 'department', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

