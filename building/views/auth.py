from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from building.forms import *


# TODO write decorator to filter unauthenticated users


def RegisterPage(request):
    """
    Defined view that handles new user registration with admin privileges.
    """

    # get admin group
    group = Group.objects.get(name='administrator')

    # instantiate new form for user registration
    form = CreateCustomUserForm()

    if request.method == 'POST':
        # pass the request method to the form
        form = CreateCustomUserForm(request.POST)

        if form.is_valid():
            new_admin_user = form.save()
            new_admin_user.groups.add(group)
            new_admin_user.save()
            # redirect user to login page after registration form is submitted
            return redirect('building:login')
    context = {'form': form}
    return render(request, 'building/auth/register.html', context)


def LoginPage(request):
    """
    Defined view that handles the user login (user with admin privileges).
    """
    if request.method == 'POST':
        # retrieve user's login credentials
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        group       = request.POST('groups')

        user = authenticate(request, username=username, password=password)

        # authenticate user if exists
        if user is not None:
            login(request, user)

            # redirect user to admin panel
            return redirect('building:admin_dashboard')

    return render(request, 'building/auth/login.html')


def LogoutUser(request):
    """
    Defined view that handles user's logout.
    """
    logout(request)
    return redirect('building:login')