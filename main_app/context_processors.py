from .models import Cart, Cartitem
from django.db.models import Sum

def cart_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        try:
            
            cart = Cart.objects.get(user=request.user, status="active")
            
            cart_count = Cartitem.objects.filter(cart=cart).aggregate(total=Sum('quantity'))['total'] or 0
        except Cart.DoesNotExist:
            cart_count = 0

    return {"cart_count": cart_count}
