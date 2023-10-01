from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

# Login Functionality
def home(request):
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
        return render(request,'home.html')
    
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
            # print(form.errors)
            messages.error(request, "You have not entered correct data for Registration")
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'Register.html', {'form':form})
    return render(request, 'Register.html')