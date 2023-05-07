from django.urls import path
from . import views 

urlpatterns = [
    # Navbar navigations
    path("",views.index, name="index"),
    path("contact/",views.contact, name="contact"),
    path("about/",views.about, name="about"),
    path("alumni_list/",views.displayAlumni, name="displayAlumni"),
    path("products/",views.ProductListView.as_view(), name="product-list"),
    # Permissions 
    path("addToEditorGroup/",views.addToEditorGroup, name="addEditorGroup"),
    path("removeFromEditorGroup/",views.removeFromEditorGroup, name="removeEditorGroup"),
    path("addToAdminGroup/",views.addToAdminGroup, name="addAdminGroup"),
    path("removeFromAdminGroup/",views.removeFromAdminGroup, name="removeAdminGroup"),
    # Profile
    path("user_profile/<int:pk>", views.displayUserProfile, name="displayUserProfile"),
    path("edit_profile/<int:pk>", views.editUserProfile, name="editUserProfile"),
    # Posts
    path("posts/",views.PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>",views.PostDetailView.as_view(), name="post-detail"),
    path("add_post/",views.PostCreateView.as_view(), name="post-create"),
    path("edit_post/<int:pk>",views.PostEditView.as_view(), name="post-edit"),
    path("delete_post/<int:pk>",views.PostDeleteView.as_view(), name="post-delete"),
    
    path("create_poll/",views.PollCreateView.as_view(), name="poll-create"),
    
    path("add_cart/<int:pk>",views.addToCart, name="addToCart"),
    path("cart/",views.CartListView.as_view(), name="cart-list"),
    path("update_cart/<int:pk>",views.updateCart, name="updateCart"),
   
]