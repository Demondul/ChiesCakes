from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = 'Flavors Page'
    return HttpResponse(response)