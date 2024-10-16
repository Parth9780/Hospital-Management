from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.shortcuts import render, redirect
from django.contrib import messages
from Hospital_Management import settings
from .forms import RegisterForm, AppointmentForm, ContactForm, UpdateProfile, forpass
from .models import *
from django.core.mail import send_mail
import random
import requests

# Create your views here.
def Signup (request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('/')  # Replace 'home' with your desired redirect URL
    else:
        form = RegisterForm()
    return render(request,'Signup.html',{'form': form})

# def Signin (request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = Register.objects.filter(email=email,password=password)
#         uid = Register.objects.get(email=email)
#         if user: #true
#             print('Login Successfuly!')
#             request.session["user"]=email #session create
#             request.session["uid"]=uid.id
#             request.session['username']=uid.username
#             return redirect('home')
#         else:
#             msg="Password and Email Are Not Match plz insert correct email or password"
#             print('error')
#     return render(request,'Signin.html')

def index (request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Register.objects.filter(email=email,password=password)
        uid = Register.objects.get(email=email)
        if user: #true
            print('Login Successfuly!')
            request.session["user"]=email #session create
            request.session["uid"]=uid.id
            request.session['username']=uid.username
            return redirect('home')
        else:
            msg="Password and Email Are Not Match plz insert correct email or password"
            print('error')
    return render(request,'index.html')

def home (request):
    username = request.session.get('username', 'Guest')
    return render(request,'Home.html',{'username':username})

def AboutUs(request):
    username = request.session.get('username', 'Guest')
    return render(request,'About.html',{'username':username})

def Services(request):
    username = request.session.get('username', 'Guest')
    return render(request,'Services.html',{'username':username})

def Appointment(request):
    username = request.session.get('username', 'Guest')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            # Email Send
            name = [request.POST['name']]
            date = [request.POST['date']]
            department = [request.POST['department']]
            # Email configuration
            subject = 'Appointment Confirmation'
            message =f"Dear {name}\nThis Mail is For Healthify Team,\nYour Appointment {department} has to {date} is SuccessFull Booked\nYou Make Sour to Comming on time To Appointment.\nany query to contact on\nkavathiyaparth852@Email.com\nparth: 6354287550"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['pp7810559@gmail.com']
            
            # Send email
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('home')  # Assuming you have a home view
    else:
        form = AppointmentForm()
    return render(request,'Appointment.html',{'form': form,'username':username})

def ContactUs(request):
    username = request.session.get('username', 'Guest')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('home')  # Replace 'home' with your home page URL name
    else:
        form = ContactForm()
    return render(request,'Contact.html',{'form': form,'username':username})

def updateProfile(request):
    user = request.session.get('user')
    uid = request.session.get('uid')
    cid=Register.objects.get(id=uid)
    if request.method=='POST':
        update = UpdateProfile(request.POST)
        if update.is_valid():
            update=UpdateProfile(request.POST,instance=cid)
            update.save()
            print('Your Profile has been Updated')
            # Email Sending to Admin
            sub = "New Contact Us"
            msg = f"Dear! New Contact is Hear. Check me out...."
            # from_Email = settings.Email_HOST_USER
            to_Email = ["pp7810559@gmail.com"]
            # to_Email = [request.POST['email']]
            
            # send_mail(subject=sub,message=msg,from_Email=from_Email,recipient_list=to_Email)
            send_mail(sub, msg, settings.EMAIL_HOST_USER, to_Email)
            return redirect('home')
        else:
            print(update.errors)
    return render(request,'updateProfile.html',{'user':user,'uid':Register.objects.get(id=uid)})

def logout_view(request):
    logout(request)
    return redirect('/')

def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Register.objects.get(email=email)
        except Register.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})
        # global otp
        global otp
        otp=random.randint(111111,999999)
        sub = "Change Our Password"
        msg = f"Dear user\nThis Mail is For Healthify Team,\nYour one time password is {otp}.\nany query to contact on\nkavathiyaparth852@Email.com\nparth: 6354287550"
        # from_Email = settings.Email_HOST_USER
        # to_Email = ["pp7810559@Email.com"]
        to_Email = [request.POST['email']]
        
        # send_mail(subject=sub,message=msg,from_Email=from_Email,recipient_list=to_Email)
        send_mail(sub, msg, settings.EMAIL_HOST_USER, to_Email)
        return redirect('/otp')
    else:
        pass
    return render(request,'forgot.html')

def otp(request):
    if request.method == 'POST':
        global otp
        eotp = ''
        for i in range(1, 7):
            eotp += request.POST.get(f'otp_{i}', '')
        stored_otp = request.session.get('otp')
        if eotp == str(otp):
            print('OTP verified successfully')
            # You might want to redirect the user to another page instead of printing to console
            return redirect('/change')
        else:
            print("Please try again")
    return render(request,'otp.html')

def change(request):
    if request.method == 'POST':
        form = forpass(request.POST)
        if form.is_valid():
            email = request.session.get('email')
            try:
                user = Register.objects.get(email=email)
                user.password = form.cleaned_data['new_password']
                user.save()
                messages.success(request, "Password updated successfully")
                return redirect('/')
            except Register.DoesNotExist:
                messages.error(request, "User not found")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = forpass()
    return render(request, 'changePassword.html', {'form': form})

def display_appointment(request):
    data = Appointment.objects.all()
    return render(request,'AppointmentView.html',{'data':data})

def UpdateAppointment(request,id):
    data = Appointment.objects.all()
    uid = Appointment.objects.get(id=id)
    if request.method=='POST':
        UpdateAppointment=AppointmentForm(request.POST)
        if UpdateAppointment.is_valid():
            UpdateAppointment.save()
            # Email Send
            Date = [request.POST['Date']]
            Name = [request.POST['Name']]
            sub = "Book Our Appointment"
            msg = f"Dear User!\nHello Dear'{Name}\nThe HealthiFy Hospetal Your Appointment {Date} is Changed\n Decose HealthiFy Hospital Dector is Not A avalible for this Data \nYou Make Sour to Comming on time To Appointment.\nany query to contact on\nhealthify0989@gmail.com\nparth: 6354287550"
            from_email = settings.EMAIL_HOST_USER
            # to_email = ["pp7810559@gmail.com"]
            to_email = [request.POST['Email']]
            
            send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to_email)
            return redirect('home')
        else:
            print(UpdateAppointment.errors)
    return render(request,'UpdateAppointment.html',{'data':data,'client':Appointment.objects.get(id=id)})

def deletedata(request,id):
    cid = Appointment.objects.get(id=id)
    Appointment.delete(cid)
    return redirect('appointmentdata')