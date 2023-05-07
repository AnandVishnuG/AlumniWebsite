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
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("dashboard/dashboard_products", views.ProductDetailView.as_view(), name="dashboard_product"),
    path("dashboard/dashboard_products_edit/<int:pk>", views.ProductEditView.as_view(), name="product-edit"),
    # path("dashboard/dashboard_products_update/<int:id>", views.product_update, name="updateProduct"),
    path("dashboard/dashboard_products_delete/<int:id>", views.product_destroy, name="deleteProduct")
]