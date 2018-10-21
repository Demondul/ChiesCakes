from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = 'Info Page!'
    return HttpResponse(response)