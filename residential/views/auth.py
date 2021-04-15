from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from residential.forms import *


def RegisterPage(request):
    """
    Defined view that handles new user registration with admin privileges.
    """

    group = Group.objects.all()

    # instantiate new form for user registration
    form = CreateUSerForm()

    # check type of method request
    if request.method == 'POST':
        # pass the request method to the form
        form = CreateUSerForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect user to login page after registration form is submitted
            return redirect('building:login')

    # context data to render in the template
    context = {'form': form}
    return render(request, 'residential/registration/register.html', context)


def LoginPage(request):
    """
    Defined view that handles the user login (user with admin privileges).
    """

    # check type of request method
    if request.method == 'POST':
        # retrieve user's login credentials
        username = request.POST.get('username')
        password = request.POST.get('password')

        # attempt user authentication
        user = authenticate(request, username=username, password=password)

        # authenticate user if exists
        if user is not None:
            login(request, user)
            # redirect admin-user to admin panel
            return redirect('building:dashboard')
    return render(request, 'residential/registration/login.html')


def LogoutUser(request):
    """
    Defined view that handles user's logout.
    """
    logout(request)
    return redirect('building:login')