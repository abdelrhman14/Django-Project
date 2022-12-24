from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *

def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, 'Congratulations,' + '   '+ username + '   ' + 'your account has been successfully created')
            #email = form.cleaned_data['email']
            #subject = 'Welcome To E6-Commerce-App'
            #body = 'Hi You have been registered successfully, We are glad to have you join us'
            #email1 = (email)
            #send_mail(
            #subject,
            #body,
            #settings.EMAIL_HOST_USER, 
            #[email1]
            #)

            # Login User
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
    
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('/products')
    else:
        form = RegisterUserForm()
    
    context = {'form':form}
    return render(request,'registration\signup.html',context)

@login_required(login_url='/accounts/login/')
def profile(request,slug):
    profile = get_object_or_404(Profile, slug=slug)
    context = {'profile':profile}
    return render(request,'registration\profile.html',context)

@login_required(login_url='/accounts/login/')
def profile_edit(request,slug):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        registerform = UserForm(request.POST,instance = request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if registerform.is_valid() and profileform.is_valid():
            registerform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect('profile',slug=slug)
    else:
        registerform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)
    return render(request,'registration/edit_profile.html',{'registerform':registerform,'profileform':profileform})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        text = request.POST['text']
        send_mail(
        name,
        text,
        settings.EMAIL_HOST_USER, 
        [email],
)

    return render(request,'registration/contact.html')

'''
        subject = 'Welcome To E6-Commerce-App'
        body = 'Hi You have been registered successfully, We are glad to have you join us'
        email = (instance.email)
 
        send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER, 
        [email],
        fail_silently=False
)
'''