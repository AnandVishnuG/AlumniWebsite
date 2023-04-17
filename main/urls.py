from django.urls import path
from . import views 

urlpatterns = [
    path("",views.index, name="index"),
    path("contact/",views.contact, name="contact"),
    path("about/",views.about, name="about"),
    path("alumni_list/",views.displayAlumni, name="displayAlumni"),
    path("user_profile/<int:pk>", views.displayUserProfile, name="displayUserProfile"),
    path("edit_profile/<int:pk>", views.editUserProfile, name="editUserProfile"),
    path("posts/",views.PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>",views.PostDetailView.as_view(), name="post-detail"),
    path("add_post/",views.PostCreateView.as_view(), name="post-create"),
    path("services/",views.ServiceListView.as_view(), name="service-list"),
    path("cart/",views.CartListView.as_view(), name="cart-list"),
]