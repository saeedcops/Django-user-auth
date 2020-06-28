from django.shortcuts import render
from django.urls import reverse

from auth_app.forms import UserProfileInfoForm,UserForm

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
# Create your views here.

def index(request):

    return render(request,'auth_app/index.html')

@login_required
def special(request):

    return HttpResponse("you'r logged in Nice!")

@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False
    if request.method == 'POST':

        user_form=UserForm(request.POST)

        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)

            user.save()

            profile =profile_form.save(commit=False)
            profile.user=user


            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True

        else:
            print(profile_form.errors,user_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'auth_app/registeration.html',{'user_form':user_form,
                                                         'profile_form':profile_form,
                                                         'registered':registered})

def user_login(request):

    if request.method =='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone try to login and field")
            print("Username:{} Password{}".format(username,password))
            return HttpResponse("Invalid Login details!")
    else:
        return render(request,'auth_app/login.html',{})