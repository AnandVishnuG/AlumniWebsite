from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from .models import Profile
# Create your views here.

def index(request):
    return render(request, "index.html",{})

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
# Display all alumni except the current logged in user
def displayAlumni(request):
    if request.user.is_authenticated:   
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "alumni_list.html",{"profiles":profiles})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')
def displayUserProfile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__id= pk)
        return render(request, "user_profile.html",{"profile":profile}) 
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')