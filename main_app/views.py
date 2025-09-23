import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import UserProfileCreationForm, ProfileForm
from .models import Category, Product, Profile, Cart, Cartitem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    all_categories_products = Category.objects.prefetch_related('product_set').all()
    return render(request, 'home.html', {"products": products,
                                         "categories": categories,
                                         "categories_products":all_categories_products})

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

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {"profile":profile})

@login_required
def edit_profile(request):
    profile = request.user.profile 

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

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
    
class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/categories/' 

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'    
# Product cbv's
class ProductList(ListView):
    model = Product
    
class ProductDetail(DetailView):
    model = Product
    
class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name','quantity','price','image','description', 'category']
    
class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name','quantity','price','image','description', 'category']

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/products/'    
    
class CartDetail(LoginRequiredMixin, DetailView):
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

@login_required
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
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = Cartitem.objects.get(id=item_id)
        cart = item.cart
        item.delete()
        cart.total_price = sum(i.price for i in cart.cartitem_set.all())
        cart.save()

    return redirect("cart-detail")
def search_suggestions(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query)[:5]  # limit to 5
    results = []
    for p in products:
        results.append({
            "id": p.id,
            "name": p.name,
            "image": p.image.url if p.image else "",
            "url": reverse("products-detail", args=[p.id]) 
        })
    return JsonResponse(results, safe=False)

@login_required
def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")
        Cart.objects.filter(user=request.user, status="active").update(
            status="completed",
        )
        return redirect("home")

@login_required
def order_history(request):
    if request.user.is_staff:
        orders = Cart.objects.filter(status="completed").order_by("-created_at")
    else:
        orders = Cart.objects.filter(user=request.user, status="completed").order_by("-created_at")
    return render(request, "main_app/order_history.html", {"orders": orders})
def all_orders(request):
    orders = Cart.objects.filter(status="completed").order_by("-created_at")
    return render(request, "orders/all_orders.html", {"orders": orders})
def update_cart_item(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_qty = int(data.get("quantity", 1))

        item = Cartitem.objects.get(id=item_id)
        item.quantity = new_qty
        item.price = new_qty * item.product.price
        item.save()

        cart = item.cart
        cart.total_price = sum(i.price for i in cart.cartitem_set.all())
        cart.save()

        return JsonResponse({
            "item_price": item.price,
            "cart_total": cart.total_price
        })