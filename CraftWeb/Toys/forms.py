from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="password",max_length=20,widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':"enter password"}))
    password2 = forms.CharField(label="Confirm password",max_length=20,widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':"reenter password"}))
    class Meta:
        model = Customer
        fields = ('Email','FirstName','LastName','Mobile','password1','password2')
        widgets = {
        'Email': forms.TextInput(attrs = {'class' : 'form-control','placeholder':"enter valid email"} ),
        'FirstName' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"first name"}),
        'LastName' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"last name"}),
        'Mobile' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"mobile"} )
        }
class CustomerLoginForm(forms.ModelForm):
    password = forms.CharField(label="password",max_length=20,widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':"enter password"}))
    class Meta:
        model = Customer
        fields = ('Email','password')
        widgets = {
        'Email': forms.TextInput(attrs = {'class' : 'form-control','placeholder':"enter valid email"} ),
        }
    def clean(self):
        if self.is_valid():
            Email=self.cleaned_data['Email']
            password = self.cleaned_data['password']
            if not authenticate(Email=Email,password=password):
                raise forms.ValidationError("invalid credentials")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['Name','Image','Price','Category','Description','Quantity']
        widgets = {
        'Name': forms.TextInput(attrs = {'class' : 'form-control' } ),
        'Price' : forms.TextInput(attrs = {'class' : 'form-control'} ),
        'Category' : forms.TextInput(attrs = {'class' : 'form-control'} ),
        'Description' : forms.TextInput(attrs = {'class' : 'form-control'} ),
        'Quantity' : forms.TextInput(attrs = {'class' : 'form-control'} ),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'Email',
        )
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=(
            'FirstName',
            'LastName',
            'Mobile', 
            )
class BillingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=(
            'Address',
            'country',
            'state',
            'city',
            'zipcode' 
            )
        widgets = {
        'Address': forms.TextInput(attrs = {'class' : 'form-control','placeholder':"Address"} ),
        'country' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"country"}),
        'state' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"state"}),
        'city' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"city"} ),
        'zipcode' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"zipcode"} ),

        }
class RequestForm(forms.ModelForm):
    class Meta:
        model=Request
        fields=(
            'ProductType',
            'Description',
        )            
        widgets = {
        'ProductType': forms.TextInput(attrs = {'class' : 'form-control','placeholder':"Type"} ),
        'Description' : forms.TextInput(attrs = {'class' : 'form-control','placeholder':"Description"}),
        }