from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = 'Profile Page!'
    return HttpResponse(response)
