from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['confirm_password']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used.')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username not available!')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password didn't matched!")
            return redirect('signup')
    
    else:
        return render(request, 'signup.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
    
        else:
            messages.info(request, 'Credentials Invalid!')
            return redirect('login')

    else:
        return render(request, 'login.html')
    
def dashboard(request):
    return render(request, 'dashboard.html')

def submit_complaint(request):
    return render(request, 'submit_complaint.html')

def my_complaint(request):
    return render(request, 'my_complaint.html')

def profile(request):
    return render(request, 'profile.html')