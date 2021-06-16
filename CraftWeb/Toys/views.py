from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
# Create your views here.
def home(req):
	if req.user.is_authenticated:
		return render(req,'index.html')
	return redirect('login')
def requestProduct(req):
	if req.user.is_authenticated:
		return render(req,'requestProduct.html')
	return redirect('login')
def register(req):
	context={}
	if req.method=="POST":
		form=CustomerRegistrationForm(req.POST)
		if form.is_valid():
			form.save()
			messages.success(req,"RECORD SAVED")
			return redirect('login')
		context['register_form'] = form
	else:
		form=CustomerRegistrationForm()
		context['register_form']=form
	return render(req,'register.html',context)
def login_view(req):
	context={}
	if req.method=="POST":
		form=CustomerLoginForm(req.POST)
		if form.is_valid():
			Email = req.POST['Email']
			password = req.POST['password']
			user = authenticate(req,Email=Email,password=password)
			if user is not None:
				login(req,user)
				return redirect('home')
		else:
			form=CustomerLoginForm()
			context['login_form']=form
			context['err']="Invalid Credentials"
	else:
		form=CustomerLoginForm()
		context['login_form'] = form
	return render(req,'login.html',context)
def logout_view(req):
	if req.user.is_authenticated:
		logout(req)
	return redirect('login')
def cart(req):
	if req.user.is_authenticated:
		return render(req,'cart.html')
	return redirect('login')
def checkout(req):
	if req.user.is_authenticated:
		return render(req,'checkout.html')
	return redirect('login')
	
def contact(req):
	return render(req,'contact.html')
def myAccount(req):
	return render(req,'my-account.html')
def productDetail(req):
	if req.user.is_authenticated:
		return render(req,'product-detail.html')
	return redirect('login')
	
def productList(req):
	if req.method == 'GET':
		products = Hotel.objects.all()
		return render(req, 'prod.html',{'Images' : products})
def paintings(req):

	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "paintings")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def kondapalli(req):
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "kondapalli")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def bottleArts(req):
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "bottleArt")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def wishlist(req):
	if req.user.is_authenticated: 
		return render(req,'wishlist.html')
	return redirect('login')
def hotel_image_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProductForm()
    return render(request, 'uploadProduct.html', {'form' : form})  
def success(request):
    return HttpResponse('successfully uploaded')

def Edit(req):
	if req.user.is_authenticated:
		return render(req , 'EditProfile.html')
	return redirect('login')
