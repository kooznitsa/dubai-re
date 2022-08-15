from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from users.models import User

from .forms import CustomUserCreationForm, ProfileForm


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('projects')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request,'Username or password is incorrect.')

    return render(request, 'users/login-register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created.')
            login(request, user)

            subject = 'Welcome to Dubai Real Estate!'
            message = f'Hi { user.username }, thank you for registering.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('edit-account')

        else:
            messages.error(request, 'An error has occurred during registration.')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)
