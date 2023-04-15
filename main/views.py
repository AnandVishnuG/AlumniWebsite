from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.views import View
from .models import Profile, Post
from .forms import PostForm, FeedbackForm
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
def editUserProfile(request, pk):
    if request.user.is_authenticated:
        # Redirect to original profile user 
        if pk != request.user.id:
            return redirect(f'/edit_profile/{request.user.id}')
            
        # Get profile object
        profile = Profile.objects.get(user__id= pk)
        
        if request.method == 'POST':
            names = request.POST['fullName'].split()
            print(names)
            profile.user.first_name = names[0]
            profile.user.last_name  = " ".join(names[1:])
            profile.user.email = request.POST['email']
            profile.avatar = request.FILES.get('avatar',None)
            profile.save()
            profile.user.save()
            messages.success(request, "Changes saved, successfully!")
        return render(request, "user_profile_edit.html",{"profile":profile}) 
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')

class PostListView( View ):
    
   def get(self, request, *args, **kwargs):
        profile = Profile.objects.all()
        posts = Post.objects.all().order_by("-created_at")
        form = PostForm()
        return render(request, 'post_list.html', {'profile':profile, 'post_list' : posts, 'form':form})
   def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-created_at")
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return render(request, 'post_list.html', {'post_list' : posts, 'form':form})

class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = FeedbackForm()
        return render(request, 'post_detail.html',{'post':post, 'form':form})
        