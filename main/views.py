from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.utils import timezone
from django.forms.models import model_to_dict
from django.forms import HiddenInput, formset_factory
from .models import Profile, Product, Post, Poll, Poll_choice, Vote, Cart, CartItem, Order, OrderItem, BillingAddress, Feedback
from .forms import PostForm, FeedbackForm, PollForm, PollChoiceForm, PollFormSet, CartForm, CartFormSet, ProductsForm, BillingAddressForm, UserForm 
from .decorators import group_required
from .mixins import CheckAdminGroupMixin, CheckEditorGroupMixin, CheckTreasurerGroupMixin, CheckAdminOrTreasurerGroupMixin, CheckAdminOrEditorGroupMixin, CheckEditorOrTreasurerGroupMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from decimal import Decimal
import pytz
import json
import requests
import os
import datetime
# Groups and Permissions
@login_required
@group_required("Admin")
def addToEditorGroup(request):
    group = Group.objects.get(name="Editor")
    request.user.groups.add(group)
    return HttpResponse("Successfully added!")

@login_required
@group_required("Admin")
def removeFromEditorGroup(request):
    group = Group.objects.get(name="Editor")
    request.user.groups.remove(group)
    return HttpResponse("Successfully removed!")

@login_required
@group_required("Admin")
def addToAdminGroup(request):
    group = Group.objects.get(name="Admin")
    request.user.groups.add(group)
    return HttpResponse("Successfully added!")

@login_required
@group_required("Admin")
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

def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        try:
            send_mail(
                subject,
                'Name: {}\nEmail: {}\n\n{}'.format(name, email, message),
                email,
                [settings.EMAIL_PRESIDENT],
                fail_silently=False,
            )
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed bro, failed!'})
    
    return JsonResponse({'success':True})


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
        profile.phone = request.POST['phone']
        profile.state = request.POST['state']
        profile.country = request.POST['country']
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
        feedbacks = Feedback.objects.filter(post= post).order_by('-created_at')
        form = FeedbackForm()
        return render(request, 'post_detail.html',{'post':post, 'form':form, 'feedbacks':feedbacks})
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        feedbacks = Feedback.objects.filter(post= post)
        comment = Feedback.objects.create(post=post, user=request.user)
        form = FeedbackForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            form= FeedbackForm()
            messages.success(request, "Comment posted!")
        return render(request, 'post_detail.html',{'post':post, 'form':form, 'feedbacks':feedbacks})
    
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
            messages.success(request, "Post successfully created!")
            return redirect('/content/')
        else:
            for field_name, errors in form.errors.items():
                if errors:
                    messages.error(f"{field_name} is not valid: {', '.join(errors)}")
        return render(request, 'add_post.html', {'form':form})

class PostEditView(LoginRequiredMixin, View):
   def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user and not request.user.groups.filter(name='Admin') and not request.user.groups.filter(name='Editor'):
            return redirect(f'/content/{pk}')
        form = PostForm(initial=model_to_dict(post))
        print(form.fields['category'])
       
        form.fields['publish_date'].widget = HiddenInput() 
        return render(request, 'edit_post.html', {'post':post, 'form':form})
   def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user and not request.user.groups.filter(name='Admin') and not request.user.groups.filter(name='Editor'):
            return redirect(f'/content/{pk}')
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        form = FeedbackForm()
        return render(request, 'post_detail.html', {'post':post, 'form':form})

class PostDeleteView(View):
   def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if post.user !=request.user and not request.user.groups.filter(name='Admin') and not request.user.groups.filter(name='Editor'):
            return redirect(f'/content/{pk}')
        post.delete()
        messages.warning(request, "Post deleted successfully!")
        return redirect('/content/')

class PollListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        polls = Poll.objects.all()
        pollChoices = Poll_choice.objects.all()
        votes = Vote.objects.all()
        
        return render(request, "display_poll.html", {'polls':polls, 'pollChoices':pollChoices, 'votes':votes})   
    def post(self, request, *args, **kwargs):
        polls = Poll.objects.all()
        pollChoices = Poll_choice.objects.all()
        if Vote.objects.filter(user=request.user.id, pollChoice = pollChoices.get(id=request.POST["choice"]) ).exists():
            messages.error(request, "You have already voted for this poll.")
            return render(request, "display_poll.html", {'polls':polls, 'pollChoices':pollChoices})   
        vote = Vote.objects.create(pollChoice= pollChoices.get(id=request.POST["choice"]), user=request.user)
        messages.success(request, "Vote successful!")
        return render(request, "display_poll.html", {'polls':polls, 'pollChoices':pollChoices})   
# Poll creation
class PollCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # poll = Poll.objects.create(user = request.user )
        # pollChoices = Poll_choice.objects.create(poll= poll)
        
        form = PollForm()
        formset = PollFormSet()
        for _, field in form.fields.items():
            if not field == form.fields["publish_date"]:
                field.widget.attrs['class'] = 'form-control'
        
        form.fields['question'].widget.attrs['placeholder'] = "Enter your question here"    
        for idx, f in enumerate(formset):
            for _, field in f.fields.items():
                field.widget.attrs['class'] = 'form-control'
            f.fields['choice'].widget.attrs['placeholder'] = f"Choice {idx+1}"    
        return render(request, 'create_poll.html',{'form':form, 'formSet':formset})
    
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.create(user = request.user )
        # pollChoices = Poll_choice.objects.filter(poll= poll)
        
        form = PollForm(request.POST, instance=poll)
        formset = PollFormSet(request.POST)
        if form.is_valid():
            pass
        else:
            for field in form.fields:
                errors = form.errors.get(field)
                if errors:
                    for error in errors:
                        print(f"Error for field {field}: {error}")
        if all([form.is_valid(), formset.is_valid()]):
            poll = form.save(commit=False)
            poll.user = request.user
            poll.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    choice = inline_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
        else: 
            print('Messed up')
                    
        return render(request, 'create_poll.html', {'form':form, 'formSet':formset})
    

# Products/Services
class ProductListView(LoginRequiredMixin, View):
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

@login_required
def deleteFromCart(request, pk):
    # Fetch the request user
    user = User.objects.get(id=request.user.id)
    # Fetch the product supplied
    cartItem = CartItem.objects.get(pk=pk)
    # Fetch cart if it exists
    cart = Cart.objects.filter(user=request.user, isPaid=False).first()
    # Fetch cart item if it exists
    # If no cart available, create new cart and increase the count
    cart.total -= ( cartItem.product.product_price * Decimal(cartItem.quantity) )   
    cartItem.delete()
    cart.count -= 1
    cart.updated_at=timezone.now()
    cart.save()
    return redirect('/cart/')
    
class CartListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user= request.user, isPaid=False).first()
        if not cart:
            messages.error(request, "You have no items in cart!")
            return redirect("/products/")
        cartItems = CartItem.objects.filter(cart=cart)
        form = CartForm(initial= model_to_dict(cart))
        formSet = CartFormSet(initial= [model_to_dict(item) for item in cartItems] if cartItems else [])
        return render(request, "cart.html", {'cart':cart, 'cartItems':cartItems, 'form':form, 'formSet':formSet})

@login_required
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

class CheckoutDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user, isPaid=False).first()
        billingAddress = BillingAddress.objects.filter(user= request.user).first()
        cartItems = CartItem.objects.filter(cart=cart)
        if not billingAddress:
            billingAddress = BillingAddress.objects.create(user= request.user)
        initial=model_to_dict(billingAddress)
        form = BillingAddressForm(instance=billingAddress)
        for _, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control mx-1'    
            
        
        return render(request, "checkout.html", {'form':form, 'cart':cart,'cartItems':cartItems})
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user, isPaid=False).first()
        billingAddress = BillingAddress.objects.filter(user= request.user).first()
        saveToDB = request.POST.get("saveToDB")
        cartItems = CartItem.objects.filter(cart=cart)
        form = BillingAddressForm(request.POST, instance=billingAddress) 
        valid= False
        for _, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control mx-1'    
            field.widget.attrs['disabled'] = True
        if form.is_valid():
            valid = True
            form.save()
        return render(request, "checkout.html", {'form':form, 'cart':cart,'cartItems':cartItems, 'valid':valid, 'saveToDB':saveToDB})

@login_required
def proceedToPay(request, form):
    billingAddress = BillingAddress.objects.filter(user= request.user).first()
    order_id = request.session.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except:
        return redirect("/cart/")
    if billingAddress:
        form = BillingAddressForm(request.POST, initial=model_to_dict(billingAddress), instance=billingAddress)
    else:
        billingAddress = BillingAddress.objects.create(user= request.user)
        form = BillingAddressForm(request.POST, instance=billingAddress)

    for _, field in form.fields.items():
        field.widget.attrs['class'] = 'form-control mx-1'    
        
    if form.is_valid():
        # form.save()
         billing_address = form.save(commit=False)
         billing_address.user = request.user
         billing_address.save()
         order.shipping_address=billing_address
         order.save()
         cart = Cart.objects.filter(user=request.user, isPaid=False).first()
         cart.isPaid = True
         cart.save()
         messages.success(request, "Payment successs!")
         return redirect("/")
    else:
        for field_name, errors in form.errors.items():
            if errors:
                print(f"{field_name} is not valid: {', '.join(errors)}")
    messages.error(request, "Payment failed!")
    return redirect("/cart/")
@login_required
def create_paypal_order(request):
    billingAddress = BillingAddress.objects.filter(user= request.user).first()
    order, isCreated = Order.objects.get_or_create(user=request.user, shipping_address=billingAddress, status="created")
    cart = Cart.objects.filter(user=request.user, isPaid=False).first()
    cartItems = CartItem.objects.filter(cart=cart)
    for item in cartItems:
        orderItem, isCreated = OrderItem.objects.get_or_create(order=order, 
                                                                product= item.product, 
                                                                quantity= item.quantity,
                                                                price=item.product.product_price,)
            
    headers = {
        "Content-Type": "application/json",
    }

    # Create the order
    payload = {
    "intent": "CAPTURE",
    "purchase_units": [
        {
            "amount": {
                "currency_code": "USD",
                "value": f"{order.get_total}",
            },
            "reference_id": str(order.id),
            "shipping": {
                "name": {
                    "full_name": f"{billingAddress.first_name} {billingAddress.last_name}",
                },
                "address": {
                    "address_line_1": billingAddress.address,
                    "admin_area_2": billingAddress.city,
                    "admin_area_1": billingAddress.state,
                    "postal_code": billingAddress.zip_code,
                    "country_code": billingAddress.country,
                }
            },
        },
    ],
}

    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",
        headers=headers,
        json=payload,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_APP_SECRET),
    )
    orderData = response.json()
    order.status = orderData["status"].capitalize()
    # Return the order ID to the client
    return JsonResponse({"id": orderData["id"]})

@csrf_exempt
def capture_paypal_order(request):
    headers = {
        "Content-Type": "application/json",
    }

    # Capture the payment
    data = json.loads(request.body)
    order_id = data["orderID"]
    
    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
        headers=headers,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_APP_SECRET),
    )
    capture_data = response.json()
    status = capture_data["status"]
    print()
    if status == "COMPLETED":
        messages.success(request, "Payment was successful!")
        order = Order.objects.get(id=capture_data["purchase_units"][0]["reference_id"])
        cart = Cart.objects.filter(user=request.user, isPaid=False).first()
        
        order.status = status.capitalize()
        order.transaction_id = capture_data["purchase_units"][0]["payments"]["captures"][0]["id"];
            
        order.save()
        cart.isPaid = True
        cart.save()
    else:
        order = Order.objects.filter(id=capture_data["purchase_units"][0]["reference_id"], status="created" ).first()
        messages.error(request, "Payment failed!")
        order.status = status.capitalize()
        order.save()
        
    # Store payment information such as the transaction ID

    # Return the capture data to the client
    return JsonResponse(capture_data)





class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard\dashboard.html", {})
        
class ProductDetailView(LoginRequiredMixin, CheckAdminOrTreasurerGroupMixin,View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        print(products)
        return render(request, 'dashboard\dashboard_product.html',{'products':products})
    
class ProductEditView(LoginRequiredMixin, CheckAdminOrTreasurerGroupMixin, View):
    def get(self, request, pk, *args, **kwargs):
            products = Product.objects.get(id = pk)
            form = ProductsForm(instance=products)
            return render(request, 'dashboard/dashboard_product_edit.html', {'products':products, 'form':form})
        
    def post(self, request, pk, *args, **kwargs):
            products = Product.objects.get(id=pk)
            form = ProductsForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/dashboard_products')
            else:
                form = ProductsForm(instance=products)
                return render(request, 'dashboard/dashboard_product_edit.html', {'form': form, 'products':products})
@login_required
@group_required(('Admin', 'Treasurer'))
def dashboard_product_add(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/dashboard_products')
    else:
        form = ProductsForm()
    return render(request, 'dashboard/dashboard_product_add.html', {'form': form})            
@login_required
@group_required(('Admin', 'Treasurer'))
def product_destroy(request, id):
         products = Product.objects.get(id=id)
         products.delete()
         return redirect('/dashboard/dashboard_products')

class FileListView(View):
    def get(self, request, *args, **kwargs):
        base_path = os.path.join(settings.MEDIA_ROOT, 'File Manager', request.user.email)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        folders = os.listdir(base_path)
        
        return render(request, "dashboard\dashboard_filemanager.html", {'folders':folders, 'uploadVisible':True} )
@login_required
def displayFolder(request, path):
    base_path = os.path.join(settings.MEDIA_ROOT, 'File Manager', request.user.email)
    folders = []
    files = []

    if '/folder/' in request.path:
        full_path = os.path.join(base_path, path)
        if os.path.exists(full_path):
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    file_path = item_path
                    if os.path.isfile(file_path):
                        file_size = os.stat(file_path).st_size
                        file_size_str = ""
                        if file_size < 1024:
                            file_size_str = f"{file_size} B"
                        elif file_size < 1024**2:
                            file_size_str = f"{round(file_size/1024, 2)} KB"
                        elif file_size < 1024**3:
                            file_size_str = f"{round(file_size/1024**2, 2)} MB"
                        else:
                            file_size_str = f"{round(file_size/1024**3, 2)} GB"

                        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                        last_modified = last_modified.strftime('%Y-%m-%d %H:%M:%S')
                        file_data = {
                            "name": os.path.basename(file_path),
                            "type": os.path.splitext(os.path.basename(file_path))[1],
                            "size": file_size_str,
                            "last_modified": last_modified,
                            "permissions": os.stat(file_path).st_mode,
                            "filepath": settings.MEDIA_URL + file_path[len(settings.MEDIA_ROOT):]
                        }
                        files.append(file_data)

    return render(request, "dashboard\dashboard_filemanager.html", {'folders': folders, 'files': files})
@login_required
def displayAlbum(request, albumname):
    images=[]
    base_path = os.path.join(settings.MEDIA_ROOT, 'Image Manager', request.user.email)
    album_path= os.path.join(base_path, albumname)
    if not os.path.isdir(album_path):
        return redirect(request, "dashboard\dashboard_imagemanager.html", {})
    for item in os.listdir(album_path):
        image={
            "filename":item,
            "url":settings.MEDIA_URL + album_path[len(settings.MEDIA_ROOT):] + "/" + item,
        }  
        images.append(image)  
    return render(request, "dashboard\dashboard_imagemanager.html", {'images': images})

class ImageListView(View):
    def get(self, request, *args, **kwargs):
        
        base_path = os.path.join(settings.MEDIA_ROOT, 'Image Manager', request.user.email)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        albums = os.listdir(base_path)
        # images = { folder:os.listdir(folder) for folder in folders}
        return render(request, "dashboard\dashboard_imagemanager.html", {'albums':albums, 'uploadVisible':True} )
class OrderListView(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, "dashboard\dashboard_orderhistory.html", {} )

@login_required
def upload_file(request):
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        uploaded_files = request.FILES.getlist('file')

        # You can customize the file storage path based on your requirements
        base_path = os.path.join(settings.MEDIA_ROOT, 'File Manager', request.user.email, folder_name)

        for uploaded_file in uploaded_files:
            fs = FileSystemStorage(location=base_path)
            fs.save(uploaded_file.name, uploaded_file)

        response = {"status": "success", "message": f"File(s) uploaded successfully."}
        return JsonResponse(response)

    return JsonResponse({"status": "error", "message": "Invalid request method."})

@login_required
def list_folders(request):
    base_path = os.path.join(settings.MEDIA_ROOT, 'File Manager', request.user.email)
    folders = os.listdir(base_path)
    return JsonResponse({"folders": folders})


@login_required
def create_folder(request):
    data=json.loads(request.body)
    if request.path == "/create_album/":
        album_name = data['albumName']
        album_path = os.path.join(settings.MEDIA_ROOT , 'Image Manager/'+request.user.email+'/'+album_name)
        if not os.path.exists(album_path):
            os.makedirs(album_path)
            response = {"status": "success", "message": f"Album '{album_name}' created successfully."}
        else:
            response = {"status": "error", "message": f"Album '{album_name}' already exists."}
    else:
        folder_name = data['folderName']
        folder_path = os.path.join(settings.MEDIA_ROOT , 'File Manager/'+request.user.email+'/'+folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            response = {"status": "success", "message": f"Folder '{folder_name}' created successfully."}
        else:
            response = {"status": "error", "message": f"Folder '{folder_name}' already exists."}

    return JsonResponse(response)
@login_required
def list_images(request):
    base_path = os.path.join(settings.MEDIA_ROOT, 'Image Manager', request.user.email)
    images = []

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append({'folder': folder, 'filename': filename})
    print(images)
    return JsonResponse({"images": images})
@login_required
def upload_image(request):
    if request.method == 'POST':
        folder_name = request.POST['album_name']
        uploaded_files = request.FILES.getlist('image')
        print(uploaded_files)
        # You can customize the file storage path based on your requirements
        base_path = os.path.join(settings.MEDIA_ROOT, 'Image Manager', request.user.email, folder_name)
        print(base_path)
        for uploaded_file in uploaded_files:
            fs = FileSystemStorage(location=base_path)
            fs.save(uploaded_file.name, uploaded_file)

        response = {"status": "success", "message": f"Image(s) uploaded successfully."}
        return JsonResponse(response)

    return JsonResponse({"status": "error", "message": "Invalid request method."})

class PermissionsView(LoginRequiredMixin, CheckAdminGroupMixin, View):
    def get( self, request, *args, **kwargs):
        users = User.objects.all()
        profiles = Profile.objects.all()
    
        roleVisible = False
        if request.user.groups.filter(name='Admin'):
            roleVisible = True
        return render(request, 'dashboard\dashboard_permissions.html', {'profiles': profiles, 'users': users, 'roleVisible': roleVisible})
@login_required
@group_required("Admin")
def user_destroy(request, id):
         user = User.objects.get(id=id)
         user.delete()
         return redirect('/dashboard_permissions')
     
class UserRoleEditView(LoginRequiredMixin, CheckAdminGroupMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(id=pk)
        userGroup = user.groups.all().first()
        groups = Group.objects.all()
        return render(request, 'dashboard/dashboard_permissions_edit.html', {'user': user, 'groups': groups, 'userGroup':userGroup})
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(id=pk)
        userGroup = user.groups.all().first()
        groups = Group.objects.all()
        
        group_name = request.POST.get("group_name")
        print(group_name)
        if group_name:
            if userGroup:
                messages.success(request, f"Already have a role!")    
                return render(request, 'dashboard/dashboard_permissions_edit.html', {'groups': groups, 'user': user, 'userGroup':userGroup})
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            user.save()
            userGroup = group_name
            messages.success(request, f"Successfully added the role {group_name} to {user.username}")
        else:
            group_remove = user.groups.all().first()
            user.groups.remove(group_remove)
            user.save()
            userGroup = ''
            messages.success(request, f"Successfully removed the roles of {user.username}")
        return render(request, 'dashboard/dashboard_permissions_edit.html', {'groups': groups, 'user': user, 'userGroup':userGroup})
@login_required
@group_required("Admin")
def dashboard_permissions_add(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['username']
        password =request.POST['password']
        if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists!")
        else:
            user = User.objects.create(username= user_name, 
                                    email= email,
                                    first_name= first_name,
                                    last_name = last_name,
                                    password= password)
            
            messages.success(request, "User successfully added!");
            return redirect('/dashboard/dashboard_permissions')
        
    return render(request, 'dashboard/dashboard_permissions_add.html', {})

class OrderHistoryView(View):
    def get( self, request, *args, **kwargs):
        if request.user.groups.filter(name__in= ('Admin', 'Treasurer')):
            orders = Order.objects.all()
            orderItems = OrderItem.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
            orderItems = OrderItem.objects.filter(order__in=orders)
        # print(users)
        return render(request, 'dashboard\dashboard_orderHistory.html', {'orders': orders, 'orderItems' : orderItems})