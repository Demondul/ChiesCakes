from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = 'Gallery Page!'
    return HttpResponse(response)
