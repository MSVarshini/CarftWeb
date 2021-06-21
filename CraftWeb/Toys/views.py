from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from CraftWeb import settings
import smtplib
from email.mime.text import MIMEText

# Create your views here.
def home(req):
	ad=False
	if req.user.is_authenticated:
		if req.user.is_admin:
			ad = True
		data = Product.objects.all()[:10]
		return render(req,'index.html',{'data':data,'ad':ad})
	return redirect('login')

def requestProduct(request):
	context={}
	ad=False
	
	if request.user.is_authenticated:
		if request.method=="POST":
			prod = request.POST['ProductType']
			desc = request.POST['Description']
			data = Request(customer=request.user,ProductType=prod,Description=desc);
			data.save()
			return redirect('/Toys/requestProduct/')
			if request.user.is_admin:
				ad = True
		return render(request,'requestProduct.html',{'ad':ad})
	return redirect('/Toys/login/')

def register(req):
	context={}
	if req.method=="POST":
		form=CustomerRegistrationForm(req.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
		context['register_form'] = form
	else:
		form=CustomerRegistrationForm()
		context['register_form']=form
	return render(req,'register.html',context)
def login_view(req):
	context={}
	ad=False
	if req.method=="POST":
		form=CustomerLoginForm(req.POST)
		if form.is_valid():
			Email = req.POST['Email']
			password = req.POST['password']
			user = authenticate(req,Email=Email,password=password)
			if user is not None:
				login(req,user)
				msg = "Successfully logged-In"
				data = Product.objects.all()[:10]
				if req.user.is_admin:
					ad=True
				return render(req,'index.html',{'data':data,'msg':msg,'ad':ad})
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
def checkout(req):
	context=""
	if req.user.is_authenticated:
		cart = Cart.objects.filter(customer=req.user)
		if not cart:
			sum1=0
			sum2=0
			return render(req,'cart.html',{'sum1':sum1,'sum2':sum1})
		sum1 = Cart.objects.filter(customer=req.user).aggregate(Sum('total'))
		if req.method=="POST":
			form = BillingForm(req.POST)
			cart = Cart.objects.filter(customer=req.user)
			tot = sum1['total__sum']
			stri=""
			for k in cart:
				cart2 = Cart.objects.get(customer=req.user,product=k.product)
				quan = cart2.quantity
				stri = stri+str(k.product.Name)+ "("+str(k.product.id)+ ")=>" + str(quan)+ '\n'+','
			if form.is_valid():
				order = Order(customer=req.user,Address=req.POST['Address'],country=req.POST['country'],state=req.POST['state'],city=req.POST['city'],zipcode=req.POST['zipcode'],productscode=stri,total=tot)
				order.save()
				stri=""
				for k in cart:
					cart2 = Cart.objects.get(customer=req.user,product=k.product)
					quan = cart2.quantity
					cart2.product.Quantity -= quan
					cart2.product.save()
					stri = stri+str(k.product.Name)+ "("+str(k.product.id)+ ")=>" + str(quan)+ '\n'+','
				Cart.objects.filter(customer=req.user).delete()
				msg = "Products Ordered Successfully"
				data = Order.objects.filter(customer=req.user).order_by('-id')
				return render(req,'orders.html',{'data':data,'msg':msg,'ad':False})
			else:
				context = "Please fill all the details"
		form = BillingForm()
		return render(req,'checkout.html',{'context':context,'form':form,'sum1':sum1['total__sum'],'sum2':sum1['total__sum']+100,'ad':False})
	return redirect('login')
	
def contact(req):
	if req.user.is_authenticated:
		return render(req,'contact.html',{'ad':False})
	return redirect('login')

def productDetail(req,id):
	ad=False
	if req.user.is_authenticated:
		data=Product.objects.get(id=id);
		if req.user.is_admin:
			ad = True
		return render(req,'product-detail.html',{'data' : data,'ad':ad})
	return redirect('login')
	
def productList(req):
	ad=False
	if req.user.is_authenticated:
		if req.user.is_admin:
			ad = True
		if req.method == 'GET':
			products = Hotel.objects.all()
			return render(req, 'prod.html',{'Images' : products,'ad':ad})
	return redirect('login')		
def paintings(req):
	ad=False
	
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "Paintings").order_by('-id')
		if req.user.is_admin:
			ad = True
		return render(req, 'prod.html',{'Images' : products,'ad':ad})
	return redirect('login')
def kondapalli(req):
	ad=False
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "Kondapalli").order_by('-id')
		if req.user.is_admin:
			ad = True
		return render(req, 'prod.html',{'Images' : products,'ad':ad})
	return redirect('login')
def bottleArts(req):
	ad=False
	
	if req.user.is_authenticated and req.method == 'GET':
		products = Product.objects.filter(Category = "BottleArts").order_by('-id')
		if req.user.is_admin:
			ad = True
		return render(req, 'prod.html',{'Images' : products,'ad':ad})
	return redirect('login')
def wishlist(req):
	if req.user.is_authenticated:
		data=Wishlist.objects.filter(customer=req.user)
		return render(req,'wishlist.html',{'data':data})
	return redirect('login')
def wishlistAdd(request, id):
	wishAdd=Wishlist.objects.filter(customer=request.user, product=Product.objects.get(id=id)).exists()
	if not wishAdd:
		wish = Wishlist(customer = request.user,product=Product.objects.get(id=id))
		wish.save()
		return redirect('/Toys/wishlist/')
		messages.success(request, 'Product Remove From Wishlist...')
	return redirect('/Toys/wishlist/')
def wishlistDel(request, id):
    Wishlist.objects.filter(customer=request.user, product=Product.objects.get(id=id)).delete()
    messages.success(request, 'Product Remove From Wishlist...')
    return redirect('/Toys/wishlist/')
def product_image_view(request):
	context={}
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			msg = "Product Added Successfully"
			return render(request, 'uploadProduct.html', {'form' : form,'msg':msg,'ad':True}) 
		else:
			form = ProductForm()
			context['error'] = 'Enter valid details'
	else:
		form = ProductForm()
	return render(request, 'uploadProduct.html', {'form' : form})  
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
			context['ad']=False
			return render(request,'EditProfile.html',context)
	else:
		form = EditProfileForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user)
		args = {}
		args['form'] = form
		args['profile_form'] = profile_form
		args['ad']=False
		return render(request, 'EditProfile.html', args)

def cart(req):
	if req.user.is_authenticated:
		data=Cart.objects.filter(customer=req.user,flag=True)
		if not data:
			sum1=0
			sum2=0
			msg = "No products are added to Cart"
			return render(req,'cart.html',{'sum1':sum1,'sum2':sum2,'msg':msg})
		sum1 = Cart.objects.filter(customer=req.user).aggregate(Sum('total'))
		return render(req,'cart.html',{'data':data,'sum1':sum1['total__sum'],'sum2':sum1['total__sum']+100,'ad':False})
	return redirect('login')
def cartAdd(request, id):
	cart_add=Cart.objects.filter(customer=request.user, product=Product.objects.get(id=id))
	prod = Product.objects.get(id=id)
	if not cart_add:
		wish = Cart(customer = request.user,product=prod,quantity=1,total=prod.Price)
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
def requests(req):
	if req.user.is_authenticated:
		ad=False
		data = Request.objects.all()
		return render(req,'requests.html',{'data':data,'ad':ad})
	return render(req,'login.html',{'ad':False})
def success(request):
    return HttpResponse('successfully uploaded')
def orders(req):
	ad=False
	if req.user.is_admin:
			ad = True
	if req.user.Email == "admin@gmail.com":
		data = Order.objects.all().order_by('-id')
		return render(req,'orders.html',{'data':data,'ad':ad})
	if req.user.is_authenticated:
		data = Order.objects.filter(customer=req.user).order_by('-id')
		return render(req,'orders.html',{'data':data,'ad':ad})
def removeOrder(req,id):
	c = Order.objects.filter(id=id).delete()
	return redirect('/Toys/orders/')
def removeRequest(req,id):
	if req.user.is_authenticated:
		c = Request.objects.filter(id=id).delete()
		return redirect('/Toys/requests/')
	return render(req,'login.html',{'ad':True})	
def getProductById(req):
	if req.method == "POST":
		title = req.POST.get("prodId")
		print(title)
		data = Product.objects.get(id=title)
		print(data)
		if data:
			return render(req,'product-detail.html',{'data':data,'ad':False})
	return redirect('/Toys/orders/')