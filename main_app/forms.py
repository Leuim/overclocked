from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserProfileCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email",required=True)
    phone = forms.CharField(label="Phone Number",max_length=20, required=False)
    address = forms.CharField(label="Address", required=False)
    image = forms.ImageField(label="Profile Image", required=False)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone", "address", "image")
        labels = {'username':'Username',
                  'email':'Email'}
        
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile 
            profile.phone = self.cleaned_data.get("phone")
            profile.address = self.cleaned_data.get("address")
            profile.image = self.cleaned_data.get("image")
            profile.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']