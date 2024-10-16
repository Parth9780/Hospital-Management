from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index),
    path('home/',views.home,name='home'),
    path('signup/',views.Signup, name='signup'),
    # path('signin/',views.Signin, name='signin'),
    path('about/',views.AboutUs,name='about'),
    path('services/',views.Services,name='services'),
    path('appointment/',views.Appointment,name='appointment'),
    path('contact/',views.ContactUs,name='contact'),
    path('updateProfile/',views.updateProfile,name='updateProfile'),
    path('logout/',views.logout_view,name='logout'),
    path('forgot/',views.forgot,name='forgot'),
    path('otp/',views.otp,name='otp'),
    path('change/',views.change,name='change'),
    path('display_appointment',views.display_appointment,name='display_appointment'),
    path('deletedata/<int:id>',views.deletedata,name='deletedata'),
    path('UpdateAppointment/<int:id>',views.UpdateAppointment,name='UpdateAppointment')
]
