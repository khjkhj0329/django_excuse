from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def calendar(request):
    return render(request, 'calendar/calendar.html')
