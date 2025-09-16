from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name="signup"),
    path('accounts/profile', views.profile, name="profile"),
    # Category cbv's 
    path('categories/create/', views.CategoryCreate.as_view(), name="categories-create"),
    path('categories/', views.CategoryList.as_view(), name='categories-index'),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name='categories-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='categories-update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='categories-delete'),
    
    # Product's cbv's
    path('products/create/', views.ProductCreate.as_view(), name="products-create"),
    path('products/', views.ProductList.as_view(), name="products-index"),
    path('products/<int:pk>', views.ProductDetail.as_view(), name="products-detail"),
    path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name='products-update'),
    path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name='products-delete'),
    
]
