from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = "Home Page!"
    return render(request, 'Home/index.html', {})