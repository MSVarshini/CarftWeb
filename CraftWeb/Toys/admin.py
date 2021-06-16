from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class MyUserAdmin(BaseUserAdmin):
	list_display=(
		'Email',
		'FirstName',
		'LastName',
		'Mobile',
		'is_admin',
		'is_active'
		)
	search_fields=('Email',
		'FirstName',
		'LastName',
		'Mobile')
	readonly_fields=('is_admin',
		'is_active')
	filter_horizontal=()
	list_filter=('is_admin',)
	fieldsets=()
	add_fieldsets=(
		(None,{
			'classes':('wide'),
			'fields' : ('Email',
		'FirstName',
		'LastName',
		'Mobile',
		'password1',
		'password2')
						}),)
	ordering=('Email',)
admin.site.register(Customer,MyUserAdmin)

# class ItemAdmin(admin.ModelAdmin):
# 	prepopulated_fields = {'slug' : {'title'}}
# 	list_dis=[
# 		'title',
# 		'Image',
# 		'Price',
# 		'Category',
# 		'Description', 
# 		'Quantity',
# 	]

# admin.site.register(Item)
# admin.site.register(Order)
# admin.site.register(OrderItem)