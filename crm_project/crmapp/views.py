from http.client import HTTPResponse
from smtplib import SMTPResponseException
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Record
from .forms import addrecord
import requests
from bs4 import BeautifulSoup
import pandas as pd 

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse

# Login Functionality
def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have login successfully")
            return redirect('home')
        else:
            messages.success(request, "Oops...Try Again!!!")
            return redirect('home')
    else:
        return render(request,'home.html', {'records':records})
    
    return render(request, 'home.html')

# Logout Functionality
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logout successfully")
    return redirect('home')

# SIGNUP FUNCTIONALITY
def Register_user(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully Register")
            return redirect('home')
        elif password1 != password2:
            messages.success(request, "Entered password is not same!!!")
            return redirect('register')
        else:
            print(form.errors)
            messages.error(request, "You have not entered correct data for Registration")
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'Register.html', {'form':form})
    return render(request, 'Register.html')

# FETCH CUSTOMER RECORD FUNCTION
def customer_record(request, id):
    if request.user.is_authenticated:
        customer_data = Record.objects.get(id=id)
        return render(request, 'record.html', {'record': customer_data})
    else:
        messages.success(request, "You must have to login to see the record..")
        return redirect('home')

# DELETE RECORD DATA
def delete_record(request, id):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=id)
        delete_record.delete()
        messages.success(request, "The selected record has been deleted.")
        return redirect('home')
    else:
        messages.success(request, "You must have to login to delete record!")
        return redirect('home')

#  ADD RECORD FUNCTION
def add_record(request):
    form = addrecord()
    if request.user.is_authenticated:
        if request.method=="POST":
            form = addrecord(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Record added successfully.....")
                return redirect('home')
            else:
                messages.success(request, "Given data is not valid.!!")
                return redirect('add')
    else:
        messages.success(request, "You must have to login to add record!")
        return redirect('home')
    return render(request, 'addrecord.html', {'form': form})

# EDIT/UPDATE RECORD FUNCTION
def update_record(request, id):
    if request.user.is_authenticated:
        cur_record = Record.objects.get(id=id)
        form = addrecord(request.POST or None, request.FILES or None, instance=cur_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect('home')
        return render(request, 'update.html', {'form':form})
    else:
        messages.success(request, "You must have to login to edit record!")
        return redirect('home')
    
#Change_Password
def Change_Password(request):
    if request.method=='POST':
     fm=PasswordChangeForm(user=request.user,data=request.POST)  
     if fm.is_valid():
          fm.save()
          update_session_auth_hash(request,fm.user)
          messages.success(request,'Your password has be changed succesfully.....') 
          return redirect('home')  
    else:
       fm=PasswordChangeForm(user=request.user)
    return render (request,'Change_Password.html',{'fm':fm})

#activate
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 