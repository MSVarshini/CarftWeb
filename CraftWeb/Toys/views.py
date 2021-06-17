from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum


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
# def cart(req):
# 	if req.user.is_authenticated:
# 		return render(req,'cart.html')
# 	return redirect('login')
def checkout(req):
	if req.user.is_authenticated and req.method=='POST':
		form = BillingForm(req.POST)
		if form.is_valid():
			data=Cart.objects.filter(customer=req.user)
			# order = Order(customer=req.user,cart=)
			sum1 = Cart.objects.filter(customer=req.user).aggregate(Sum('total'))
		return render(req,'checkout.html',{'form':form,'sum1':sum1['total__sum'],'sum2':sum1['total__sum']+100})
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
		products = Product.objects.filter(Category = "Paintings")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def kondapalli(req):
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "Kondapalli")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def bottleArts(req):
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "BottleArts")
		print(products)
		return render(req, 'prod.html',{'Images' : products})
	return redirect('login')
def wishlist(req):
	if req.user.is_authenticated:
		data=Wishlist.objects.filter(customer=req.user)
		print(data)
		return render(req,'wishlist.html',{'data':data})
	return redirect('login')
def wishlistAdd(request, id):
	print("FWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.id)
	print(type(id))
	#print(Product.objects.get(id=id))
	wishAdd=Wishlist.objects.filter(customer=request.user, product=Product.objects.get(id=id)).exists()
	print(wishAdd is None)
	if not wishAdd:
		wish = Wishlist(customer = request.user,product=Product.objects.get(id=id))
		print(wish)
		wish.save()
		return redirect('/Toys/wishlist/')
		messages.success(request, 'Product Remove From Wishlist...')
	return redirect('/Toys/wishlist/')
def wishlistDel(request, id):
    Wishlist.objects.filter(customer=request.user, product=Product.objects.get(id=id)).delete()
    messages.success(request, 'Product Remove From Wishlist...')
    return redirect('Toys//wishlist')
def hotel_image_view(request):
	context={}
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('success')
		else:
			form = ProductForm()
			context['error'] = 'Enter valid details'
	else:
		form = ProductForm()
	return render(request, 'uploadProduct.html', {'form' : form})  
def success(request):
    return HttpResponse('successfully uploaded')

def Edit(req):
	if req.user.is_authenticated:
		return render(req , 'EditProfile.html')
	return redirect('login')


def edit_profile(request):
	context={}
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)  # request.FILES is show the selected image or file
		if form.is_valid() and profile_form.is_valid():
			user_form = form.save()
			custom_form = profile_form.save(False)
			custom_form.user = user_form
			custom_form.save()
			context['msg'] = "Updated your Profile successfully"
			return render(request,'EditProfile.html',context)
	else:
		form = EditProfileForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user)
		args = {}
		args['form'] = form
		args['profile_form'] = profile_form
		return render(request, 'EditProfile.html', args)

def cart(req):
	if req.user.is_authenticated:
		data=Cart.objects.filter(customer=req.user)
		sum1 = Cart.objects.filter(customer=req.user).aggregate(Sum('total'))
		print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",sum1['total__sum'])
		return render(req,'cart.html',{'data':data,'sum1':sum1['total__sum'],'sum2':sum1['total__sum']+100})
	return redirect('login')
def cartAdd(request, id):
	#print("FWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",request.user.id)
	print(type(id))
	print(Product.objects.get(id=id))
	cart_add=Cart.objects.filter(customer=request.user, product=Product.objects.get(id=id))
	print(cart_add)
	prod = Product.objects.get(id=id)
	if not cart_add:
		wish = Cart(customer = request.user,product=prod,quantity=1,total=prod.Price)
		print(wish)
		wish.save()
		return redirect('/Toys/cart/')
		messages.success(request, 'Product Added From Cart...')
	else:
		c = Cart.objects.get(customer = request.user,product=prod)
		quan = c.quantity
		c.quantity = quan+1
		c.total += prod.Price
		c.save()
	return redirect('/Toys/cart/')
def cartDel(request, id):
    cart_del = Cart.objects.get(customer=request.user, product=Product.objects.get(id=id))
    prod = Product.objects.get(id=id)
    quan = (cart_del.quantity)-1
    print(quan)
    if quan==0:
    	Cart.objects.get(customer=request.user, product=Product.objects.get(id=id)).delete()
    else:
    	c=Cart.objects.get(customer = request.user,product=Product.objects.get(id=id))
    	Cart.objects.get(customer=request.user, product=Product.objects.get(id=id)).delete()
    	c.quantity = quan
    	c.total -= prod.Price
    	c.save()
    	
    messages.success(request, 'Product Remove From Cart...')
    return redirect('/Toys/cart/')
def remove(request,id):
	Cart.objects.get(customer=request.user, product=Product.objects.get(id=id)).delete()
	return redirect('/Toys/cart/')