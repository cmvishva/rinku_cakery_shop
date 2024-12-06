"""
URL configuration for rinku_cakery_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from rinku_cakery_admin.views import *
from rinku_cakery_user.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('admin_change_password', admin_change_password,name='admin_change_password'),
    path('adminlogin', adminlogin,name="adminlogin"),
    path('adminregister', adminregister,name="adminregister"),
    path('admin_logout', admin_logout,name="admin_logout"),
    
    path('dashboard', dashboard,name='dashboard'),
    path('add_main_menu', add_mainmenu,name='add_main_menu'),
    path('view_main_menu', view_mainmenu,name='view_main_menu'),
    path('delete_main_menu/<int:id>', view_mainmenu,name='delete_main_menu'),
    path('update_main_menu/<int:id>', update_mainmenu,name='update_main_menu'),
    path('add_product', addproduct,name='add_product'),
    path('view_product', viewproduct,name='view_product'),
    path('deleteproduct/<int:id>', deleteproduct,name='deleteproduct'),
    path('updateproduct/<int:uid>', updateproduct,name='updateproduct'),
    path('productby_category/<int:category_id>', productby_category,name='productby_category'),
    path('add_category', add_category,name='add_category'),
    path('delete_category/<int:id>', delete_category,name='delete_category'),
    path('update_category/<int:id>', update_category,name='update_category'),
    path('view_category', view_category,name='view_category'),
    path('add_slider', addslider,name='add_slider'),
    path('view_slider',viewslider,name='view_slider'),
    path('deleteslider/<int:id>',deleteslider,name='deleteslider'), 
    path('updateslider/<int:id>',updateslider,name='updateslider'), 
    
    path('view_about_header_img',view_about_header_img,name='view_about_header_img'), 
    path('add_about_header_img',add_about_header_img,name='add_about_header_img'),  
    path('update_about_header_img/<int:id>',update_about_header_img,name='update_about_header_img'), 
    path('delete_about_header_img/<int:id>',delete_about_header_img,name='delete_about_header_img'),
    
    path('view_about_sec1',view_about_sec1,name='view_about_sec1'), 
    path('add_about_sec1',add_about_sec1,name='add_about_sec1'),  
    path('update_about_sec1/<int:id>',update_about_sec1,name='update_about_sec1'), 
    path('delete_about_sec1/<int:id>',delete_about_sec1,name='delete_about_sec1'),
    
    path('view_about_sec2',view_about_sec2,name='view_about_sec2'), 
    path('add_about_sec2',add_about_sec2,name='add_about_sec2'),  
    path('update_about_sec2/<int:id>',update_about_sec2,name='update_about_sec2'), 
    path('delete_about_sec2/<int:id>',delete_about_sec2,name='delete_about_sec2'), 
    
    path('add_cart_header_img',add_cart_header_img,name='add_cart_header_img'), 
    path('view_cart_header_img',view_cart_header_img,name='view_cart_header_img'),  
    path('update_cart_header_img/<int:id>',update_cart_header_img,name='update_cart_header_img'), 
    path('delete_cart_header_img/<int:id>',delete_cart_header_img,name='delete_cart_header_img'),
    
    path('add_contact_header_img',add_contact_header_img,name='add_contact_header_img'), 
    path('view_contact_header_img',view_contact_header_img,name='view_contact_header_img'),   
    path('update_contact_header_img/<int:id>',update_contact_header_img,name='update_contact_header_img'), 
    path('delete_contact_header_img/<int:id>',delete_contact_header_img,name='delete_contact_header_img'),
    
    path('add_contact_middele_img',add_contact_middele_img,name='add_contact_middele_img'), 
    path('view_contact_middele_img',view_contact_middele_img,name='view_contact_middele_img'),  
    path('view_contact_middele_img',view_contact_middele_img,name='view_contact_middele_img'),  
    path('update_contact_middele_img/<int:id>',update_contact_middele_img,name='update_contact_middele_img'), 
    path('delete_contact_middele_img/<int:id>',delete_contact_middele_img,name='delete_contact_middele_img'),
    
    path('view_contact_address_info',view_contact_address,name='view_contact_address_info'), 
    path('add_contact_address_info',add_contact_address,name='add_contact_address_info'), 
    path('update_contact_address_info/<int:id>',update_contact_address,name='update_contact_address_address'), 
    path('delete_contact_address_info/<int:id>',delete_contact_address,name='delete_contact_address_address'),
    
    path('view_contact_messages',view_contact_messages,name='view_contact_messages'), 
    path('delete_contact_messages/<int:id>',delete_contact_messages,name='delete_contact_messages'),
    
    path('view_orders',view_orders,name='view_orders'),
    path('delete_orders/<int:order_id>',delete_orders,name='delete_orders'),
    
    path('viewfooter',viewfooter,name='viewfooter'), 
    path('addfooter',addfooter,name='addfooter'), 
    path('updatefooter/<int:id>',updatefooter,name='updatefooter'), 
    path('deletefooter/<int:id>',deletefooter,name='deletefooter'), 
    
    path('view_hygiene_sec_bg_img',view_hsimage,name='view_hygiene_sec_bg_img'), 
    path('add_hygiene_sec_bg_img',add_hsimage,name='add_hygiene_sec_bg_img'), 
    path('update_hygiene_sec_bg_img/<int:id>',update_hsimage,name='view_hygiene_sec_bg_img'), 
    path('delete_hygiene_sec_bg_img/<int:id>',delete_hsimage,name='view_hygiene_sec_bg_img'), 
    
    path('order_fulldetails/<int:user_id>/<int:order_id>', view_orders_fulldetails, name='order_fulldetails'),

    
    # +==================== User =========================+\
        
    path('user_register', user_register,name="user_register"),
    # path('registeruser', registeruser,name="registeruser"),
    path('userlogin', userlogin,name="userlogin"),
    path('userlogout', userlogout,name="userlogout"),
    path('send_otp', send_otp,name="send_otp"),
    path('enter_otp', enter_otp,name="enter_otp"),
    path('forgot_password', forgot_password,name="forgot_password"),
    path('password_reset', password_reset,name="password_reset"),
    path('index', index,name="index"),
    path('', index,name="index"),
    path('about',about_page,name="about"),
    path('contact',contact_page,name="contact"),
    path('order_page/<int:product_id>',order_page,name="order_page"),
    path('cart_page',cart_page,name="cart_page"), 
    path('our_cakes',our_cakes,name="our_cakes"),
    path('addtocart/<int:user_id>/<int:product_id>/',add_to_cart,name="addtocart"),
    path('delete_cart_item/<int:item_id>',delete_cart_item,name="delete_cart_item"),
    # path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),
    # path('decrement/<int:user_id>/<int:product_id>/', item_decrement, name='decrement'),
    # path('increment/<int:user_id>/<int:product_id>/', item_increment, name='increment'),
    
    path('generate_pdf/<int:user_id>', generate_pdf, name='generate_pdf'),
    path('order_confirmation/<int:user_id>', order_confirmation, name='order_confirmation'),
    path('checkout_page_data/<int:user_id>', checkout_page_data, name='checkout_page_data'),
    path('checkout_page/<int:user_id>', checkout_page, name='checkout_page'),
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)