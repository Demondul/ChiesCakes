from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response='Reviews Page!'
    return HttpResponse(response)
