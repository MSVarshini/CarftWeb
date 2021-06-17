from django.urls import path
from Toys import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
	path('home/',views.home,name="home"),
	path('login/',views.login_view,name="login"),
	path('logout/',views.logout_view,name="logout"),
	path('register/',views.register,name="register"),
	#path('login1/',views.login1,name="login1"),
	# path('register1/',views.register1,name="register1"),
	path('requestProduct/',views.requestProduct,name="requestProduct"),
	#path('cart/',views.cart,name="cart"),
	path('checkout/',views.checkout,name="checkout"),
	path('contact/',views.contact,name="contact"),
	path('myAccount/',views.myAccount,name="myAccount"),
	path('productDetail/',views.productDetail,name="productDetail"),
	path('productList/',views.productList,name="productList"),
	path('paintings/',views.paintings,name="paintings"),
	path('kondapalli/',views.kondapalli,name="kondapalli"),
	path('bottleArts/',views.bottleArts,name="bottleArts"),
	path('wishlist/',views.wishlist,name='wishlist'),
	path('wishlistDel/<int:id>',views.wishlistDel,name="wishlistDel"),
	path('wishlistAdd/<int:id>',views.wishlistAdd,name="wishlistAdd"),
	path('cart/',views.cart,name='cart'),
	path('cartDel/<int:id>',views.cartDel,name="cartDel"),
	path('cartAdd/<int:id>',views.cartAdd,name="cartAdd"),
	path('image_upload/', views.hotel_image_view, name = 'image_upload'),
    path('success/', views.success, name = 'success'),
    path('Edit/', views.edit_profile, name = 'Edit'),
    path('remove/<int:id>', views.remove, name = 'remove'),

]
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)