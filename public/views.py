from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from public.forms import user_registration_form
from dash.models import Category, Job_Listing
from chats.models import Profile

# Create your views here.

def home(request):
    categories = Category.objects.annotate(
        posted_jobs_count = Count('job_listing', filter=Q(job_listing__status='posted'))
    )

    if request.user.is_authenticated:
        featured_jobs = Job_Listing.objects.exclude(created_by=request.user).filter(featured_status=True)

    else:
        featured_jobs = Job_Listing.objects.filter(featured_status=True)

    context = {'categories': categories, 'featured_jobs': featured_jobs}
    return render(request, 'public_home.html', context)


def register(request):
    register_form = user_registration_form()

    if request.method == "POST":
        register_form = user_registration_form(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect('sign_in')

    return render(request, 'public_register.html', {'register_form': register_form})


def sign_in(request):
    login_form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

        if user:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password')

    context = {'sign_in_form': login_form}
    return render(request, 'public_sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')
 
