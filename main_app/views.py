from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
         form = UserCreationForm()
           
    context = {'form':form}
    return render(request, 'signup.html', context)        

def all_categories(request):
    categories = Category.objects.all()
    return render(request, "category/index.html", categories)


# Category cbv's
class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    
class CategoryDetail(DetailView):
    model = Category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.product_set.all()
        return context
    
class CategoryList(ListView):
    model = Category
    
class CategoryDelete(DeleteView):
    model = Category
    success_url = '/categories/' 

class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'    
# Product cbv's
class ProductList(ListView):
    model = Product
    
class ProductDetail(DetailView):
    model = Product
    
class ProductCreate(CreateView):
    model = Product
    fields = ['name','quantity','price','image','description', 'category']
    
class ProductUpdate(UpdateView):
    model = Product
    fields = ['name','quantity','price','image','description', 'category']

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'    