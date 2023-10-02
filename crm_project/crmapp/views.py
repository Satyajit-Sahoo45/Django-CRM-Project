from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .forms import addrecord
from .models import Record

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