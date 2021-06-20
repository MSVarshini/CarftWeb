from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

CATEGORY_CHOICES = (
		('Kondapalli','Kondapalli'),
		('BottleArts' , 'BottleArts'),
		('Paintings','Paintings'),
	)

class MyUserManager(BaseUserManager):
	def create_user(self,Email,FirstName,LastName,Mobile,password = None):
		if not Email:
			raise ValueError("Email is required")
		elif not FirstName:
			raise ValueError("FirstName is required")
		elif not LastName:
			raise ValueError("LastName is required")
		elif not Mobile:
			raise ValueError("Mobile is required")
		user = self.model(
			Email = self.normalize_email(Email),
			FirstName = FirstName,
			LastName = LastName,
			Mobile =Mobile
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self,Email,FirstName,LastName,Mobile,password = None):
		user = self.create_user(
			Email = Email,
			FirstName = FirstName,
			LastName = LastName,
			Mobile =Mobile,
			password=password
		)
		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
class Customer(AbstractBaseUser):
	Email = models.EmailField(null=False,unique=True,max_length=30)
	FirstName=models.CharField(max_length=20,unique=True)
	LastName=models.CharField(max_length=20)
	Mobile=models.CharField(max_length=10)
	is_admin=models.BooleanField(default=False)
	is_active=models.BooleanField(default=True)
	is_staff=models.BooleanField(default=False)
	is_superuser=models.BooleanField(default=False)
	USERNAME_FIELD = 'Email'
	REQUIRED_FIELDS = ['FirstName','LastName','Mobile']
	objects = MyUserManager()
	def __str__(self):
		return str(self.Email)
	def has_perm(self,perm,obj=None):
		return True
	def has_module_perms(self,app_label):
		return True
class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')
class Product(models.Model):
	Name=models.CharField(max_length=20,unique=True)
	Image = models.ImageField(upload_to='images/',unique=True)
	Price=models.IntegerField()
	Category=models.CharField(choices = CATEGORY_CHOICES, max_length=20)
	Description = models.TextField()
	Quantity = models.IntegerField()

	def __unicode__(self):
		return self.title
	def get_price(self):
		return self.Price
class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
    	return str(self.id)
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1,null=False)
    total = models.DecimalField(max_digits = 100,decimal_places = 2,default=0.00)
    flag = models.BooleanField(default=True)
    def __str__(self):
    	return str(self.id)
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	Address = models.TextField(null=False,max_length=50)
	country = models.CharField(null=False,max_length=50)
	state = models.CharField(null=False,max_length=50)
	city = models.CharField(null=False,max_length=50)
	zipcode = models.IntegerField(null=False)
	productscode = models.TextField(max_length=100,null=False)
	total = models.DecimalField(max_digits = 100,decimal_places = 2,default=0.00)
class Request(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	ProductType = models.CharField(max_length=20)
	Description = models.TextField(null=False,max_length=200)
		