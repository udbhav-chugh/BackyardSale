from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse("<h1>Backyard Sale: Coming SOON!!</h1>")
