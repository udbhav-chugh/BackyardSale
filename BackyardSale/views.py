from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout



def home(request):
    return HttpResponse("<h1>Backyard Sale: Coming SOON!!</h1>")


def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Hello " + user.username)
            else:
                return render(request, 'DashBoard/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request,'DashBoard/login.html', {'error_message':"Invalid Username Password"})
    else:
        return render(request,'DashBoard/login.html')