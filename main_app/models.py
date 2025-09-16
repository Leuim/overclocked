from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField( max_length=20, blank=True, null=True)
    address = models.CharField( blank=True, null=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Cart
class Cart(models.Model):
    total_price = models.IntegerField()
    # do the choice's once known
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart belongs to {self.user}"


# Order
class Order(models.Model):
    total_price = models.IntegerField()
    status = models.CharField(max_length=50)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Order belongs {self.cart}"


# Category 
class Category(models.Model):
    name = models.CharField()
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('categories-detail', kwargs={'pk': self.id})
    
    
# Product
class Product(models.Model):
    name = models.CharField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products-detail', kwargs={'pk': self.id})
 

# Cartitem 
class Cartitem(models.Model):
    quantity = models.IntegerField()
    price = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart item is {self.product} quantity: {self.quantity} price: {self.price}"