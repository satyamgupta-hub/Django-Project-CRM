from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CreateUserForm,LoginUser,CreateRecordForm,UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Record
from django.contrib import messages

def home(request):
    return render(request,'webapp/index.html',{})

def register(request):

    # get the instance of form created in the forms.py
    form = CreateUserForm()
    # check the request comes from the post method
    if request.method == "POST":
        # now get the everyhing from the form 
        form = CreateUserForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # if valid then save it and redirect to loginpage
            form.save()
            messages.success(request,'You are successfully Registered!')
            return redirect('loginpage') 
    
    # now take the data into the register page
    context = {'form':form}
    # otherwise we will again register
    return render(request,'webapp/register.html',context=context)

def login(request):
    form = LoginUser()
    if request.method=="POST":
        form = LoginUser(request,data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Let's check is the user is already into our system or not
            user = authenticate(request,username=username,password=password)

            # if already rgister thn simple login and redirect to the dashboardpage 
            if user is not None:
                auth.login(request,user)
                messages.success(request,'You are successfully Login!')
                return redirect('dashboardpage')
                # return dashboard page
    context = {'form2':form}
    return render(request,'webapp/login.html',context=context)

def logoutUser(request):
    auth.logout(request)
    messages.success(request,'You are exist successfully!')
    return redirect('loginpage')

@login_required(login_url='loginpage')
def dashboardView(request):
    # retrieve all the records from the Records Model
    my_records = Record.objects.all()
    context= {'records':my_records}                                                                                
    return render(request,'webapp/dashboard.html',context=context)

# create a record
@login_required(login_url='loginpage')
def create_record(request):
    # if data is came with the POST request
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboardpage")
    # if data is not came theny simple move to the create-record page for the user to enter records
    context={'form':form}
    return render(request,'webapp/create_records.html',context=context)

# read or view a single Records
@login_required(login_url='loginpage')
def view_single_record(request,pk):
    # fetching the record with the id 
    all_records= Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request,'webapp/records-views.html',context)

@login_required(login_url='loginpage')
def update_record(request,pk):
    # fetch specific record based on te primary key
    record_need_to_update = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record_need_to_update)
    if request.method =="POST":
        form = UpdateRecordForm(request.POST,instance=record_need_to_update)
        if form.is_valid():
            form.save()
            messages.success(request,'Your records are updated successfully!')
            redirect('dashboardpage')
    
    context={'form':form}
    return render(request,'webapp/update-records.html',context)

@login_required(login_url='loginpage')
def delete_record(request,pk):
    record_need__to_delete = Record.objects.get(id=pk)
    record_need__to_delete.delete()
    messages.success(request, "Your record was deleted!")
    return redirect('dashboardpage')
