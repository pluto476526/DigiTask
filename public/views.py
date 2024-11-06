from django.shortcuts import render, redirect
from public.forms import user_registration_form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'public_home.html')


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

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password')

    context = {'sign_in_form': login_form}
    return render(request, 'public_sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')
 