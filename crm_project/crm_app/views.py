from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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