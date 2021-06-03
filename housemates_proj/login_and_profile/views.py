import re
from .models import User, Item, HouseMembership, House, BalanceDue, BalanceOwed
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

################### Login Methods ###################


def index(request):
    return render(request, "login.html")


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validation(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['this_userid'] = new_user.id
        request.session['this_first_name'] = new_user.first_name
        messages.success(request, "You have successfully registered!")
        return redirect('/profile')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    messages.success(request, "You have successfully logged in!")
    return redirect('/profile')


def logout(request):
    request.session.clear()
    return redirect('/')


################### Profile Methods ###################


def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        # add notifications?
        'user': User.objects.get(id=request.session['user_id'])
    }
    # add if statement to redirect to main_house if existing
    return render(request, 'profile.html', context)


def create_house(request):
    pass


def main_house(request, id):
    pass
