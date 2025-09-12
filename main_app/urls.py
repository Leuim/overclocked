from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name="signup"),
    
    # Category cbv's 
    path('categorys/create/', views.CategoryCreate.as_view(), name="categorys-create"),
    path('categorys/', views.CategoryList.as_view(), name='categorys-index'),
    path('categorys/<int:pk>', views.CategoryDetail.as_view(), name='categorys-detail'),
]
