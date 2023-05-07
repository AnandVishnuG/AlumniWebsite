from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.forms.models import model_to_dict
from django.forms import HiddenInput, formset_factory
from .models import Profile, Product, Post, Poll_choice, Cart, CartItem
from .forms import PostForm, FeedbackForm, PollForm, PollChoiceForm, PollFormSet, CartForm, CartFormSet, ProductsForm
from .decorators import group_required
from .mixins import CheckAdminGroupMixin, CheckEditorGroupMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import pytz
import json

# Groups and Permissions
@login_required
def addToEditorGroup(request):
    group = Group.objects.get(name="Editor")
    request.user.groups.add(group)
    return HttpResponse("Successfully added!")

@login_required
def removeFromEditorGroup(request):
    group = Group.objects.get(name="Editor")
    request.user.groups.remove(group)
    return HttpResponse("Successfully removed!")

@login_required
def addToAdminGroup(request):
    group = Group.objects.get(name="Admin")
    request.user.groups.add(group)
    return HttpResponse("Successfully added!")

@login_required
def removeFromAdminGroup(request):
    group = Group.objects.get(name="Admin")
    request.user.groups.remove(group)
    return HttpResponse("Successfully removed!")

@login_required
@group_required("Admin")
def addUser(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password1']
        confirmPassword = request.POST['password2']
        if password != confirmPassword:
            messages.warning(request, "Passwords don't match!")
            return HttpResponse("Passwords don't match!")            
        try:
            if User.objects.get(username=name):
                messages.warning(request, "User already exist!")
                return render(request, "authentication/signup.html")            
        except Exception as ide:
            pass            
        user = User.objects.create_user(name, email, password)
        user.save()    
    return HttpResponse("Successfully added!")
@login_required
@group_required("Admin")
def deleteUser(request):
    if request.method == 'POST':
        name = request.POST["name"]
        user = User.objects.remove(username=name)
    return HttpResponse("Successfully removed!")
# Website general views
def index(request):
    return render(request, "index.html",{})

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

# Display list of Alumni
@login_required
def displayAlumni(request):
# Display all alumni except the current logged in user
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "alumni_list.html",{"profiles":profiles})
# Display user profile
@login_required
def displayUserProfile(request, pk):
    profile = Profile.objects.get(user__id= pk)
    return render(request, "user_profile.html",{"profile":profile}) 
# Edit user profile
@login_required
def editUserProfile(request, pk):
    # Redirect to original profile user 
    if pk != request.user.id:
        return redirect(f'/edit_profile/{request.user.id}')
        
    # Get profile object
    profile = Profile.objects.get(user__id= pk)
    
    if request.method == 'POST':
        names = request.POST['fullName'].split()
        profile.user.first_name = names[0]
        profile.user.last_name  = " ".join(names[1:])
        profile.user.email = request.POST['email']
        profile.linkedin_url = request.POST['linkedin_url']
        profile.instagram_url = request.POST['instagram_url']
        profile.twitter_url = request.POST['twitter_url']
        profile.state = request.POST['state']
        profile.country = request.POST['country']
        if request.FILES.get('avatar',None) != None:
            profile.avatar = request.FILES.get('avatar',None)
        profile.save()
        profile.user.save()
        messages.success(request, "Changes saved, successfully!")
    return render(request, "user_profile_edit.html",{"profile":profile}) 

class PostListView( View ):
   def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-publish_date").filter(publish_date__lte=timezone.now().astimezone(pytz.utc))
        print(posts[0].created_at)
        print(posts[0].publish_date)
        print(timezone.now().astimezone(pytz.utc))
        print(len(posts))
        
        form = PostForm()
        return render(request, 'post_list.html', {'post_list' : posts, 'form':form})
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
    
class PostCreateView(View): 
   def get(self, request, *args, **kwargs):
        form = PostForm(request.POST) 
        return render(request, 'add_post.html', {'form':form})
   def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return render(request, 'add_post.html', {'form':form})

class PostEditView(View):
   def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user:
            return redirect(f'/posts/{pk}')
        form = PostForm(initial=model_to_dict(post))
        print(form.fields['category'])
       
        form.fields['publish_date'].widget = HiddenInput() 
        return render(request, 'edit_post.html', {'post':post, 'form':form})
   def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user:
            return redirect(f'/posts/{pk}')
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        form = FeedbackForm()
        return render(request, 'post_detail.html', {'post':post, 'form':form})

class PostDeleteView(View):
   def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user:
            return redirect(f'/posts/{pk}')
        post.delete()
        messages.warning(request, "Post deleted successfully!")
        return redirect('/posts/')
   
# Poll creation
class PollCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PollForm()
        formset = PollFormSet(queryset=Poll_choice.objects.none())
        
        return render(request, 'create_poll.html',{'form':form, 'formSet':formset})
    
    def post(self, request, *args, **kwargs):
        form = PollForm(request.POST)
        formset = PollFormSet(data=self.request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            poll = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    choice = inline_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
        return render(request, 'create_poll.html', {'form':form, 'formSet':formset})
    

# Products/Services
class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'products.html',{'products':products}) 

@login_required
def addToCart(request, pk):
    # Fetch the request user
    user = User.objects.get(id=request.user.id)
    # Fetch the product supplied
    product = Product.objects.get(pk=pk)
    # Fetch cart if it exists
    cart = Cart.objects.filter(user=request.user, isPaid=False).first()
    # Fetch cart item if it exists
    cartItem = CartItem.objects.filter(cart=cart, product=product).first()
    # If no product is passed, redirect without adding anything
    if not product:
        return redirect('/products/')
    # If no cart available, create new cart and increase the count
    if not cart:
        cart = Cart.objects.create(user=user, created_at=timezone.now(), updated_at=timezone.now())
        cart.count += 1
        cart.total += product.product_price
        cart.save()
        cartItem = CartItem.objects.create(cart=cart, product=product)
        cartItem.save()        
    # If cart exists
    else:
        # If it is a new cart item
        if not cartItem:
            cartItem = CartItem.objects.create(cart=cart, product=product)
            cart.count += 1
        # Existing cart item 
        else:
            print(cartItem)
            cartItem.quantity += 1    
            cartItem.save()
        
        cart.updated_at=timezone.now()
        cart.total += product.product_price
        cart.save()
    return redirect('/products/')    
class CartListView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user= request.user, isPaid=False).first()
        cartItems = CartItem.objects.filter(cart=cart)
        form = CartForm(initial= model_to_dict(cart))
        formSet = CartFormSet(initial= [model_to_dict(item) for item in cartItems] if cartItems else [])
        return render(request, "cart1.html", {'cart':cart, 'cartItems':cartItems, 'form':form, 'formSet':formSet})

def updateCart(request, pk):
    data = json.loads(request.body)
    cartItemId = data['cartItemId']
    cartItemQuantity = data['cartItemQuantity']
    cart = Cart.objects.get(user= request.user, pk=pk, isPaid=False)
    cartItem = CartItem.objects.filter(cart=cart, id=cartItemId).first()
    cart.total = Decimal(cart.total) - ( cartItem.product.product_price * Decimal(cartItem.quantity) )
    cartItem.quantity = cartItemQuantity
    cartItem.save()    
    cart.total = Decimal(cart.total) + ( cartItem.product.product_price * Decimal(cartItem.quantity) )
    cart.save()
    response_data = {
        'message': 'Item updated',
        'total': cart.total,
    }
    return JsonResponse(response_data, safe=False)
    

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard\dashboard.html", {})
    
class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        print(products)
        return render(request, 'dashboard\dashboard_product.html',{'products':products})
    
class ProductEditView(View):
        
    def get(self, request, pk, *args, **kwargs):
            products = Products.objects.get(id = pk)
            form = ProductsForm(instance=products)
            return render(request, 'dashboard/dashboard_product_edit.html', {'products':products, 'form':form})
        
    def post(self, request, pk, *args, **kwargs):
            products = Products.objects.get(id=pk)
            form = ProductsForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/dashboard_products')
            else:
                form = ProductsForm(instance=products)
                return render(request, 'dashboard/dashboard_product_edit.html', {'form': form, 'products':products})
            
def product_destroy(request, id):
         products = Products.objects.get(id=id)
         products.delete()
         return redirect('/dashboard/dashboard_products')