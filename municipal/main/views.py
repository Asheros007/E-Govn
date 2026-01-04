from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Complaint

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
    
@login_required
def dashboard(request):

    user_complaints = Complaint.objects.filter(user=request.user)
    
    total_complaints = user_complaints.count()
    pending_count = user_complaints.filter(status='PENDING').count()
    in_progress_count = user_complaints.filter(status='IN_PROGRESS').count()
    resolved_count = user_complaints.filter(status='RESOLVED').count()
    rejected_count = user_complaints.filter(status='REJECTED').count()
    
    recent_complaints = user_complaints.order_by('-created_at')[:5]
    
    context = {
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'rejected_count': rejected_count,
        'recent_complaints': recent_complaints,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def submit_complaint(request):
    if request.method == 'POST':

        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if not category or not description:
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'submit_complaint.html')
        
        complaint = Complaint.objects.create(
            user=request.user,
            category=category,
            description=description,
            image=image,
            status='PENDING'
        )
        
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('my_complaint')
    
    return render(request, 'submit_complaint.html')

@login_required
def my_complaint(request):

    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    status_filter = request.GET.get('status', None)
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    total_count = Complaint.objects.filter(user=request.user).count()
    pending_count = Complaint.objects.filter(user=request.user, status='PENDING').count()
    in_progress_count = Complaint.objects.filter(user=request.user, status='IN_PROGRESS').count()
    resolved_count = Complaint.objects.filter(user=request.user, status='RESOLVED').count()
    rejected_count = Complaint.objects.filter(user=request.user, status='REJECTED').count()
    
    context = {
        'complaints': complaints,
        'status_filter': status_filter,
        'total_count': total_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'rejected_count': rejected_count,
    }
    
    return render(request, 'my_complaint.html', context)

@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    
    context = {
        'complaint': complaint,
    }
    
    return render(request, 'complaint_detail.html', context)

def user_logout(request):
    logout(request)
    return redirect('landing')