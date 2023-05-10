from django.urls import path
from . import views 

urlpatterns = [
    # Navbar navigations
    path("",views.index, name="index"),
    path("contact/",views.contactUs, name="contact"),
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
    path("content/",views.PostListView.as_view(), name="post-list"),
    path("content/<int:pk>",views.PostDetailView.as_view(), name="post-detail"),
    path("add_post/",views.PostCreateView.as_view(), name="post-create"),
    path("edit_post/<int:pk>",views.PostEditView.as_view(), name="post-edit"),
    path("delete_post/<int:pk>",views.PostDeleteView.as_view(), name="post-delete"),
    
    path("create_poll/",views.PollCreateView.as_view(), name="poll-create"),
    path("display_poll/",views.PollListView.as_view(), name="poll-list"),
    
    path("add_cart/<int:pk>",views.addToCart, name="addToCart"),
    path("delete_cart/<int:pk>",views.deleteFromCart, name="deleteFromCart"),
    path("cart/",views.CartListView.as_view(), name="cart-list"),
    path("update_cart/<int:pk>",views.updateCart, name="updateCart"),
    
   
    path("checkout/",views.CheckoutDetailView.as_view(), name="checkout-detail"),
    path("proceed_pay/",views.proceedToPay, name="proceedToPay"),
    path("create_paypal_order/",views.create_paypal_order, name="createPaypalOrder"),
    path("capture_paypal_order/",views.capture_paypal_order, name="capturePaypalOrder"),
    
    
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("dashboard/dashboard_products", views.ProductDetailView.as_view(), name="dashboard_product"),
    path("dashboard/dashboard_products_edit/<int:pk>", views.ProductEditView.as_view(), name="product-edit"),
    path('dashboard/dashboard_products_add/', views.dashboard_product_add, name='dashboard_product_add'),
    path("dashboard/dashboard_products_delete/<int:id>", views.product_destroy, name="deleteProduct"),
    path("dashboard/dashboard_filemanager/", views.FileListView.as_view(), name="file-list"),
    path("dashboard/dashboard_imagemanager/", views.ImageListView.as_view(), name="image-list"),
    path("dashboard/dashboard_orderhistory/", views.OrderListView.as_view(), name="order-list"),
    
    path("dashboard/dashboard_permissions/", views.PermissionsView.as_view(), name="dashboard_permissions"),
    path('dashboard/dashboard_permissions_add/', views.dashboard_permissions_add, name='dashboard_permissions_add'),
    path("dashboard/dashboard_permissions_edit/<int:pk>", views.UserRoleEditView.as_view(), name="permissions-edit"),
    path("dashboard/dashboard_permissions_delete/<int:id>", views.user_destroy, name="deleteUser"),
    path("dashboard/order_history/", views.OrderHistoryView.as_view(), name="order_history"),   
    
    path('list_images/', views.list_images, name='list_images'),
    path('create_folder/', views.create_folder, name='create_folder'),
     path('create_album/', views.create_folder, name='create_folder'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('folder/<path:path>/', views.displayFolder, name="displayFolder" ),   
    path('album/<albumname>/', views.displayAlbum, name="displayAlbum" ),   
    path('upload_image/', views.upload_image, name='upload_image'),
    
]