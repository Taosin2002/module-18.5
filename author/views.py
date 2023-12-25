from django.shortcuts import render,redirect
from .forms import RegisterForm,ChangeUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,"")
            return redirect('login')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form,'type':'Register'})

@login_required
def profile(request):
    return render(request,'profile.html')

def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            user_name=form.cleaned_data['username']
            user_pass=form.cleaned_data['password']
            user=authenticate(username=user_name,password=user_pass)
            if user is not None:
                messages.success(request,"Logged In Successfully")
                login(request,user)
                return redirect('profile')
            else:
                messages.warning(request,"Password Incorrect")
                return redirect('register')
    else:
        form=AuthenticationForm()
    return render(request,'register.html',{'form':form,'type':'Login'})

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        form = ChangeUserForm(instance = request.user)
    return render(request, 'edit_profile.html', {'form' : form})

def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : form})