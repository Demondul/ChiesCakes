from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = 'Reservations Page!'
    return HttpResponse(response)