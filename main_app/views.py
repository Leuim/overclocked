from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileCreationForm
from .models import Category, Product, Profile, Cart, Cartitem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def signup(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
         form = UserProfileCreationForm()
           
    context = {'form':form}
    return render(request, 'signup.html', context)        

def all_categories(request):
    categories = Category.objects.all()
    return render(request, "category/index.html", categories)

def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {"profile":profile})

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
    
class CartDetail(DetailView):
    model= Cart
    template_name = "main_app/cart_detail.html"
    context_object_name = "cart"
    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            status="active",
            defaults={"total_price": 0}
        )
        return cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    qty = int(request.POST.get("quantity", 1)) 
    cart, _ = Cart.objects.get_or_create(user=request.user, status="active", defaults={"total_price": 0})
    item, created = Cartitem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": qty, "price": product.price * qty})
    if not created:
        item.quantity += qty
        item.price = item.quantity * product.price
        item.save()
    cart.total_price = sum(i.price for i in cart.cartitem_set.all())
    cart.save()
    return redirect('cart-detail')

def search_suggestions(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query)[:5]  # limit to 5
    results = []
    for p in products:
        results.append({
            "id": p.id,
            "name": p.name,
            "image": p.image.url if p.image else ""
        })
    return JsonResponse(results, safe=False)