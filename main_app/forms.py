from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField( required=False)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone", "address")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile 
            profile.phone = self.cleaned_data.get("phone")
            profile.address = self.cleaned_data.get("address")
            profile.save()
        return user
