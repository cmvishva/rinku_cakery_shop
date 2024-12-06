from email.message import EmailMessage
from gettext import translation
import os
import random
from django.conf import settings
from django.shortcuts import render

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Create your views here.
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

from django.shortcuts import render, HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image,Spacer
from reportlab.lib.colors import Color
from reportlab.lib.colors import black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
import os

# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()

import json
import logging

logger = logging.getLogger(__name__)
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from rinku_cakery_user.models import *
# from .models import LogEntry
from django.contrib.admin.models import LogEntry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rinku_cakery_admin.models import *



from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib import messages as django_messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.urls import reverse

import time

import os
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# Create your views here.



# ==================================== user register =============================================




from django.shortcuts import render, redirect

from django.contrib import messages

def registeruser(request):
    if 'username' in request.POST:
        username = request.POST['username']
    else:
        username = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        mobile = request.POST['mobile']
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            mobile=mobile
        )
        user.save()
        return redirect("/userlogin/")
    return render(request,"user/register.html")

from django.contrib.auth.hashers import make_password

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        
        raw_password = request.POST['password']
        password = make_password(raw_password)
        
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/user_register')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('/user_register')

        user = UserProfile.objects.create(
            username=username,
            email=email,
            phone=phone,
            password=password
        )

        # You might want to store the phone number in a profile model or an additional field.
        # Assuming you have a Profile model with a OneToOne relationship to User.
        # Profile.objects.create(user=user, phone=phone)

        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('/userlogin')

    return render(request, "user/register.html")

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout

from django.contrib.auth import get_user_model
# from Rinku_Cakery_Admin.models import User


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = UserProfile()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User authentication successful, log in the user
            login(request, user)
            return redirect('cart_page')  # Redirect to the index page after successful login
        else:
            print("Authentication failed:", user)  # Inspect the user object for details
            messages.error(request, 'Invalid credentials')

    return render(request, 'user/login.html')

def userlogout(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect("index")

# ============================================  SEND OTP =============================
from django.core.mail import send_mail, EmailMessage
def send_otp(request):
    if request.method == "POST":
        email = request.POST['email']
        user_email = UserProfile.objects.filter(email=email).first()
        if user_email:
            otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
            # otp = random.randint(11111, 99999)
            user_email.otp = otp
            user_email.save()
            request.session['email'] = email
            html_message = f"Your OTP is: {otp}"
            subject = "Forgot Password OTP"
            email_to = [email]
            try:
                message = EmailMessage(subject, html_message, to=email_to)
                message.send()
                messages.success(request, 'OTP sent to your email.')
                return redirect('/enter_otp')
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")
                return redirect('/forgot_password')
        else:
            messages.error(request, "Invalid Email")
            return render(request, 'user/forgot_password.html')
    return render(request, 'user/forgot_password.html')

        
    
# =============================  Forget Password =========================
   
def forgot_password(request):
    return render(request,"user/forgot_password.html")     

# =============================  Enter OTP =========================

def enter_otp(request):
    user_otp = None
    if request.session.has_key('email'):
        email = request.session.get('email')  # Retrieve the email from the session
        print("Email from session:", email)

        user = UserProfile.objects.filter(email=email)
        
        if user.exists():
            user_otp = user.first().otp
        
        if request.method == "POST":
            otp = request.POST.get('otp')
            if not otp: 
                messages.error(request, "OTP is Required")
            elif user_otp is None:
                messages.error(request, "User not found")
            elif user_otp != otp:
                messages.error(request, "Invalid OTP")
            else:
                return render(request, "user/password_reset.html")
        return render(request, 'user/enter_otp.html')
    else:
        return redirect('/login')
    
# def enter_otp(request):
#     error_message =None
#     user_otp = None
#     if request.session.has_key('email'):
#         email = request.POST.get('email')
        
#         email = request.session.get('email')  # Retrieve the email from the session
#         print("Email from session:", email)

#         user = UserProfile.objects.filter(email=email)
        
#         if user.exists():
#             user_otp = user.first().otp
        
#         if request.method == "POST":
#             otp = request.POST.get('otp')
#             if not otp: 
#                 error_message = "OTP is Required"
#             elif user_otp is None:
#                 error_message = "User not found"  # Handle case where user is not found
#             elif user_otp != otp:
#                 error_message = "Invalid OTP"
#             if not error_message:
#                 # return redirect("/password_reset")
#                 return render(request,"user/password_reset.html")
#         return render(request,'user/enter_otp.html',{'error_message':error_message})


# ================================ Change Password ===========================   
from django.contrib.auth.hashers import make_password, check_password
def password_reset(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = UserProfile.objects.get(email=email)
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if not new_password:
                messages.error(request, "Enter New Password")
            elif not confirm_new_password:
                messages.error(request, "Enter Confirm New Password")
            elif check_password(new_password, user.password):
                messages.error(request, "This Password Already Exists Try New Password")
            elif new_password != confirm_new_password:
                messages.error(request, "Passwords Do Not Match")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password Changed Successfully")
                html_message = "Your Password Changed Successfully"
                subject = "Change Password"
                email_to = [email]
                message = EmailMessage(subject, html_message, to=email_to)
                message.send()
                return render(request, "user/password_reset.html", {'success_message': "Password Changed Successfully"})
    return render(request, "user/password_reset.html")

# def password_reset(request):
#     if request.session.has_key('email'):
#         email = request.session['email']
#         user = UserProfile.objects.get(email=email)
#         if request.method == "POST":
#             new_password = request.POST.get('new_password')
#             confirm_new_password = request.POST.get('confirm_new_password')
#             if not new_password:
#                 messages.error(request, "Enter New Password")
#             elif not confirm_new_password:
#                 messages.error(request, "Enter Confirm New Password")
#             elif new_password == user.password:
#                 messages.error(request, "This Password Already Exists Try New Password")
#             elif new_password != confirm_new_password:
#                 messages.error(request, "Passwords do not match")
#             else:
#                 user.password = make_password(new_password)
#                 user.save()
#                 messages.success(request, "Password Changed Successfully")
#                 html_message = "Your Password Changed Successfully"
#                 subject = "Change Password"
#                 email_to = [email]
#                 message = EmailMessage(subject, html_message, to=email_to)
#                 message.send()
#                 return render(request, "user/password_reset.html")
#     return render(request, "user/password_reset.html")
    
# def password_reset(request):
#     error_message = None
#     if request.session.has_key('email'):
#         email = request.session['email']
#         user = UserProfile.objects.get(email=email)
#         if request.method == "POST":
#             new_password = request.POST.get('new_password')
#             confirm_new_password = request.POST.get('confirm_new_password')
#             new_password_hash = make_password(new_password)
#             if not new_password_hash:
#                 error_message = "Enter New Password"
#             elif not confirm_new_password:
#                 error_message = "Enter Confirm New Password"
#             elif new_password_hash == user.password:
#                 error_message = "This Password Already Exists Try New Password"
#             if not error_message:
#                 user.password = new_password_hash
#                 user.save()
#                 messages.success(request,"Password Changed Successfully")
#                 html_message = "Your Password Changed Successfully"
#                 subject = "Change Password"
#                 email_to = [email]
#                 message = EmailMessage(subject,html_message,email_to)
#                 message.send()
#                 return redirect("/userlogin")
#     return render(request,"user/password_reset.html",{'error':error_message})
                


# ====================================  User =======================================================

def index(request):
    viewpd = Product.objects.all()
    viewsd = Sliders.objects.all()
    viewmenu = Main_menu.objects.all()
    latest_slider_instance = Sliders.objects.last()
    hygien_bg = bh_background.objects.last()
    footerimg = Footerimg.objects.last()
    
    paginator = Paginator(viewpd, 8)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,"user/index.html",{"viewpd":viewpd,"viewsd":viewsd,"viewmenu":viewmenu,'slider_instance': latest_slider_instance,"footerimg":footerimg,"hygien_bg":hygien_bg,"page_obj":page_obj})

def about_page(request):
    viewmenu = Main_menu.objects.all()
    hygien_bg = bh_background.objects.last()
    header_img = aboutheader.objects.last() 
    about_sec1 = Aboutsec1.objects.last()    
    about_sec2 = Aboutsec2.objects.last()    
    footerimg = Footerimg.objects.last()
    return render(request,"user/about_page.html",{"viewmenu":viewmenu,"header_img":header_img,"about_sec1":about_sec1,"about_sec2":about_sec2,"footerimg":footerimg,"hygien_bg":hygien_bg})

from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField



def contact_page(request):
    viewmenu = Main_menu.objects.all()
    contact_header_img = contactheader.objects.last()
    contact_middeleimg = contactmiddle.objects.last()
    footerimg = Footerimg.objects.last()
    viewcontact_address = contact_address.objects.last()
    cm = contact_message_data()

    if request.method == "POST":
        cm = contact_message_data(request.POST, request.FILES)
        if cm.is_valid():
            cm.save()
            django_messages.success(request, 'Your message has been sent successfully!')
            return redirect('/contact')
        else:
            print(cm.errors)
    
    return render(request,"user/contact_page.html",{"viewmenu":viewmenu,"cm":cm,"contact_header_img":contact_header_img,"contact_middeleimg":contact_middeleimg,"footerimg":footerimg,"viewcontact_address":viewcontact_address})


def order_page(request,product_id):
    viewmenu = Main_menu.objects.all()
    footerimg = Footerimg.objects.last()
    viewpd = Product.objects.get(id=product_id)
    
    base_price_500gm = viewpd.pprice
    
    price_1kg = base_price_500gm * 2  # Price for 1kg is double the price for 500g
    price_1_5kg = base_price_500gm * 3  # Price for 1.5kg is 1.5 times the price for 1kg
    price_2kg = base_price_500gm * 4  # Price for 2kg is double the price for 1kg
    price_2_5kg = base_price_500gm * 5  # Price for 2.5kg is 1.25 times the price for 2kg
    price_3kg = base_price_500gm * 6  # Price for 3kg is double the price for 1.5kg
    price_3_5kg = base_price_500gm * 7  # Price for 3.5kg is 1.17 times the price for 3kg
    price_4kg = base_price_500gm * 8
    prices = {
        '500gm': base_price_500gm,
    '1kg': price_1kg,
    '1.5kg': price_1_5kg,
    '2kg': price_2kg,
    '2.5kg': price_2_5kg,
    '3kg': price_3kg,
    '3.5kg': price_3_5kg,
    '4kg': price_4kg,
    }
    # selected_weight = request.GET.get('weight')
    # print(selected_weight)
   
    weights = []
    if viewpd:
        if viewpd.pweight_500gm:
            weights.append('500gm')
        if viewpd.pweight_1kg:
            weights.append('1kg')
        if viewpd.pweight_1_5kg:
            weights.append('1.5kg')
        if viewpd.pweight_2kg:
            weights.append('2kg')
        if viewpd.pweight_2_5kg:
            weights.append('2.5kg')
        if viewpd.pweight_3kg:
            weights.append('3kg')
        if viewpd.pweight_3_5kg:
            weights.append('3.5kg')
        if viewpd.pweight_4kg:
            weights.append('4kg')
        if viewpd.pweight_4_5kg:
            weights.append('4.5kg')
        if viewpd.pweight_5kg:
            weights.append('5kg')
    
    # weights = Product.objects.values_list('pweight', flat=True).distinct()
    # weights= [viewpd.pweight]
    if not request.user.is_authenticated:
        return redirect('/userlogin')  # Redirect to login page if the user is not authenticated

    user_id = request.user.id
    add_to_cart_url = reverse('addtocart', kwargs={'user_id': user_id, 'product_id': product_id})
    
    return render(request,"user/order_page.html",{"viewmenu":viewmenu,"viewpd":viewpd,'prices': prices, "weights":weights,'add_to_cart_url': add_to_cart_url,'product_id': product_id,
        'user_id': user_id,"footerimg":footerimg})


def our_cakes(request):
    category = Category.objects.all()
    viewmenu = Main_menu.objects.all()
    footerimg = Footerimg.objects.last()
    viewpd = Product.objects.all()
    
    paginator = Paginator(viewpd, 8)  # Show 10 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"user/our_cakes.html",{"category":category,"viewmenu":viewmenu,"footerimg":footerimg,"page_obj":page_obj})

def productby_category(request,category_id):
    viewmenu = Main_menu.objects.all()
    cat = get_object_or_404(Category,id=category_id)
    viewpd = Product.objects.filter(catfk=cat)
    category = Category.objects.all()
    
    paginator = Paginator(viewpd, 8)  # Show 10 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"user/our_cakes.html",{"cat":cat,"viewpd":viewpd,"category":category,"page_obj":page_obj,"viewmenu":viewmenu})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse


@login_required(login_url="/userlogin")
def cart_page(request):
    viewmenu = Main_menu.objects.all()
    # cart_items = Cart_Data.objects.all()
    cart_header_img = cartheader.objects.last()  
    footerimg = Footerimg.objects.last()
    # user = userdata.objects.filter(id=user_id)
    
    cart_items = Cart_Data.objects.filter(user=request.user)
   
    is_empty_cart = len(cart_items) == 0
    
    if not is_empty_cart:
        for item in cart_items:
            item.total_price = item.selected_price * item.product_qty
    
    overall_total = sum(item.total_price for item in cart_items)
    
    order_items = orders_item.objects.filter(user=request.user)
    
    current_date = datetime.now().strftime("%B %d, %Y")
    # total_price = sum(int(item.selected_price) * int(item.product_qty) for item in cart_items)
    return render(request,"user/cart_page.html",{"viewmenu":viewmenu,"cart_header_img":cart_header_img,"footerimg":footerimg,"cart_items": cart_items,"overall_total": overall_total,"order_items":order_items,"current_date":current_date,
        "is_empty_cart": is_empty_cart,})

@login_required(login_url="/userlogin")
def add_to_cart(request, user_id, product_id):
    try:
        user = User.objects.get(id=user_id)  # Assuming your user model is named User
        product = Product.objects.get(id=product_id)
        selected_weight = request.POST.get('selected_weight')
        selected_price = request.POST.get('selected_price')
        message = request.POST.get('message')
       
        # Check if all required data is available
        if user and product and selected_weight:
            cart_item, created = Cart_Data.objects.get_or_create(
                user=user,
                product=product,
                selected_weight=selected_weight,
                defaults={'product_qty': 1, 'selected_price': selected_price, 'message': message}
            )

            if not created:
                response = {"status": "info", "message": "Product already in cart."}
            else:
                response = {"status": "success", "message": "Product added to cart successfully."}
        else:
            response = {"status": "error", "message": "Please Select Weight."}

        return JsonResponse(response)

    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found. Please check the user ID."}, status=404)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"}, status=500)

def calculate_overall_total(user):
    cart_items = Cart_Data.objects.filter(user=user)
    overall_total = sum(item.total_price for item in cart_items)
    return overall_total

# def item_increment(request, product_id, user_id):
#     try:
#         cart_item = Cart_Data.objects.get(product_id=product_id, user_id=user_id)
#         cart_item.product_qty += 1
#         cart_item.save()
#         return redirect('cart_page')
#     except Cart_Data.DoesNotExist:
#         return render(request, 'user/cart_page.html', {'error_message': 'Cart item not found.'})
#     except Exception as e:
#         return render(request, 'user/cart_page.html', {'error_message': str(e)})

# def item_decrement(request, product_id,user_id):
#     # items = CartItem.objects.get(id=id)
    
#     cart_item = Cart_Data.objects.get(product_id=product_id,user_id=user_id)
#     quantity = cart_item.product_qty
#     if quantity:
#         cart_item.product_qty -= 1 
#         cart_item.save()
#         return redirect('cart_page')
#     return render(request,'user/cart_page.html')


def delete_cart_item(request,item_id):
    del_cart_item = Cart_Data.objects.get(id=item_id).delete()
    return redirect('cart_page')
    return render(request,"user/cart_page.html")
    
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
@login_required

# def update_cart_quantity(request):
#     item_id = request.POST.get('item_id')
#     quantity = request.POST.get('quantity')

#     # Update quantity in the database
#     cart_item = Cart_Data.objects.get(id=item_id)
#     cart_item.quantity = quantity
#     cart_item.save()

#     # Calculate total price for the item and return it
#     total_price = cart_item.price * cart_item.quantity

#     return JsonResponse({'total_price': total_price})




# =======================================================  checkout page  ============================================================
 
@login_required(login_url="/userlogin")
def checkout_page(request, user_id):
    viewmenu = Main_menu.objects.all()
    cart_header_img = cartheader.objects.last()  
    footerimg = Footerimg.objects.last()
    user = get_object_or_404(UserProfile, id=user_id)

    cart_items = Cart_Data.objects.filter(user=user)
    is_empty_cart = len(cart_items) == 0
    if not is_empty_cart:
        for item in cart_items:
            item.total_price = item.selected_price * item.product_qty

    overall_total = sum(item.total_price for item in cart_items) 
    current_date = datetime.now().strftime("%B %d, %Y")
    return render(request, "user/checkout.html", {
        "viewmenu": viewmenu,
        "cart_header_img": cart_header_img,
        "footerimg": footerimg,
        "cart_items": cart_items,
        "overall_total": overall_total,
        "current_date": current_date,
        "is_empty_cart": is_empty_cart,
    })
    
@login_required(login_url="/userlogin")    
def checkout_page_data(request, user_id):   
    viewmenu = Main_menu.objects.all()
    cart_header_img = cartheader.objects.last()  
    footerimg = Footerimg.objects.last()
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        cart_items = Cart_Data.objects.filter(user=user)
        is_empty_cart = len(cart_items) == 0
        if not is_empty_cart:
            for item in cart_items:
                total_price = item.selected_price * item.product_qty
            for cart_item in cart_items:
                order = orders_item(
                    user=user,
                    fname=fname,
                    lname=lname,
                    email=email,
                    phone=phone,
                    address=address,
                    product=cart_item.product,
                    price=cart_item.selected_price,
                    weight=cart_item.selected_weight,
                    quantity=cart_item.product_qty,
                    total_price=total_price,
                    message=cart_item.message
                )
                order.save()
            return redirect(reverse('order_confirmation', args=[user_id]))

    # Handling GET request
    cart_items = Cart_Data.objects.filter(user=user)
    is_empty_cart = len(cart_items) == 0
    if not is_empty_cart:
        for item in cart_items:
            item.total_price = item.selected_price * item.product_qty

    overall_total = sum(item.total_price for item in cart_items) 
    current_date = datetime.now().strftime("%B %d, %Y")
    return render(request, "user/checkout.html", {
        "viewmenu": viewmenu,
        "cart_header_img": cart_header_img,
        "footerimg": footerimg,
        "cart_items": cart_items,
        "overall_total": overall_total,
        "current_date": current_date,
        "is_empty_cart": is_empty_cart,
    }) 
 
# @login_required(login_url="/userlogin")    
# def checkoutpage(request,user_id):   
#     viewmenu = Main_menu.objects.all()
#     cart_header_img = cartheader.objects.last()  
#     footerimg = Footerimg.objects.last()
    
#     if request.method == 'POST':
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         address = request.POST['address']
#         # cart = request.session.get('cart')
#         user = get_object_or_404(UserProfile, id=user_id)
#         cart_items = Cart_Data.objects.filter(user=user)
#         # products = product_data.objects.filter()
#         # products = product_data.get_products_by_id(cart.keys())
#         is_empty_cart = len(cart_items) == 0
#         if not is_empty_cart:
#             for item in cart_items:
#                 total_price = item.selected_price * item.product_qty
#             for cart_item in cart_items:
#                 order = orders_item(
#                     user = user,
#                     fname=fname,
#                     lname=lname,
#                     email=email,
#                     phone=phone,
#                     address=address,
#                     product = cart_item.product,
#                     price = cart_item.selected_price,
#                     weight = cart_item.selected_weight,
#                     quantity = cart_item.product_qty,
#                     total_price = total_price,
#                     message=cart_item.message
#                 )
#                 order.save()
#             return redirect(reverse('order_confirmation', args=[user_id]))
    
    
#     # user = userdata.objects.filter(id=user_id)
    
#     cart_items = Cart_Data.objects.filter(user=request.user)
   
#     is_empty_cart = len(cart_items) == 0
    
#     if not is_empty_cart:
#         for item in cart_items:
#             item.total_price = item.selected_price * item.product_qty
    
#     overall_total = sum(item.total_price for item in cart_items) 
#     current_date = datetime.now().strftime("%B %d, %Y")
#     return render(request,"user/checkout.html",{"viewmenu":viewmenu,"cart_header_img":cart_header_img,"footerimg":footerimg,"cart_items": cart_items,"overall_total": overall_total,"current_date":current_date,
#         "is_empty_cart": is_empty_cart,})
    
# ======================================================  checkout page End =======================================================

    
 # =====================================================  order confirmation =====================================================
@login_required(login_url="/userlogin")
def order_confirmation(request, user_id):
    # Fetch necessary data
    viewmenu = Main_menu.objects.all()
    cart_header_img = cartheader.objects.last()
    footerimg = Footerimg.objects.last()

    # Fetch the user based on user_id
    user_profile = get_object_or_404(UserProfile, id=user_id)

    # Filter cart items for the specified user
    cart_items = Cart_Data.objects.filter(user=user_profile)

    is_empty_cart = len(cart_items) == 0

    # Calculate total prices for items in the cart
    if not is_empty_cart:
        for item in cart_items:
            item.total_price = item.selected_price * item.product_qty

    # Calculate overall total
    overall_total = sum(item.total_price for item in cart_items)

    # Current date
    current_date = datetime.now().strftime("%B %d, %Y")

    return render(request, "user/order_confirmation.html", {
        "viewmenu": viewmenu,
        "cart_header_img": cart_header_img,
        "footerimg": footerimg,
        "cart_items": cart_items,
        "overall_total": overall_total,
        "is_empty_cart": is_empty_cart,
        "current_date": current_date,
    })
    

# ================================ Generate Pdf =============================================


@login_required(login_url="/userlogin")
def generate_pdf(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        try:
            # Retrieve user's order details
            order_items = Cart_Data.objects.filter(user=request.user)
            user_info = orders_item.objects.filter(user=request.user).last()
            contact_address_details = contact_address.objects.last()

            # Calculate overall total
            overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
            current_date = datetime.now().strftime("%m/%d/%Y")

            # Create the PDF document
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

            # Create a canvas to draw on
            pdf_canvas = canvas.Canvas(response, pagesize=letter)
            width, height = letter

            # Set background color
            background_color = Color(242/255, 250/255, 215/255)  # Convert #fff3cd to RGB
            pdf_canvas.setFillColor(background_color)
            pdf_canvas.rect(0, 0, width, height, fill=1)

            light_green = Color(153/255, 255/255, 153/255)  # RGB values for light green
            pdf_canvas.setFillColor(light_green)

            y_position = height - 100
            logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')  # replace with your logo file path
            logo_width, logo_height = 70, 90  # adjust the size of the logo
            pdf_canvas.drawImage(logo_path, 50, y_position, logo_width, logo_height)

            # Draw header text
            pdf_canvas.setFillColorRGB(89/255, 116/255, 69/255)
            pdf_canvas.setFont("Helvetica-BoldOblique", 24)  # bold, italic font
            pdf_canvas.drawString(200, height - 70, "Rinku's Cakery Shop")

            y_coord = height - 170 

            # Set font and font size
            pdf_canvas.setFont("Helvetica", 12)
            pdf_canvas.setFillColorRGB(89/255, 116/255, 69/255)

            # Draw invoice header
            pdf_canvas.drawString(50, y_coord, "Email:")
            pdf_canvas.drawString(150, y_coord, f"{user.email}")
            
            y_coord -= 20
            pdf_canvas.drawString(50, y_coord, "FIRST NAME:")
            pdf_canvas.drawString(150, y_coord, f"{user_info.fname}")

            y_coord -= 20  # move down to the next line
            pdf_canvas.drawString(50, y_coord, "LAST NAME:")
            pdf_canvas.drawString(150, y_coord, f"{user_info.lname}")

            y_coord -= 20  # move down to the next line
            pdf_canvas.drawString(50, y_coord, "PHONE:")
            pdf_canvas.drawString(150, y_coord, f"{user_info.phone}")

            y_coord -= 20  # move down to the next line
            pdf_canvas.drawString(50, y_coord, "ADDRESS:")
            pdf_canvas.drawString(150, y_coord, f"{user_info.address}")

            # Set initial y position for items
            y_position = height - 390
            item_row_height = 120  # Height of each item row including image and text

            # Draw item table data
            for item in order_items:
                # Check if the item will fit on the current page; if not, start a new page
                if y_position - item_row_height < 100:
                    pdf_canvas.showPage()  # End the current page and start a new one
                    pdf_canvas.setFillColor(background_color)
                    pdf_canvas.rect(0, 0, width, height, fill=1)
                    y_position = height - 110  # Reset y_position

                # Calculate the x-coordinate for the image and text
                image_x = 130  # Position image 50 pixels from the left edge
                text_x = image_x + 190  # Position text to the right of the image

                # Define the image size
                image_width, image_height = 150, 100  # Adjust the size of the image

                # Define the border color and width
                border_color = Color(0, 0, 0)  # Black
                border_width = 3

                # Draw the rounded rectangle (border)
                pdf_canvas.setLineWidth(border_width)
                pdf_canvas.setStrokeColor(border_color)
                pdf_canvas.roundRect(image_x, y_position, image_width, image_height, 0, fill=0)

                # Draw image
                image_path = os.path.join(settings.MEDIA_ROOT, str(item.product.pimage))
                pdf_canvas.drawImage(image_path, image_x, y_position, image_width, image_height)

                # Draw text
                pdf_canvas.drawString(text_x, y_position + image_height - 15, item.product.pname)
                pdf_canvas.drawString(text_x, y_position + image_height - 35, "Quantity: " + str(item.product_qty))
                pdf_canvas.drawString(text_x, y_position + image_height - 55, "Price: " + str(item.selected_price))
                pdf_canvas.drawString(text_x, y_position + image_height - 75, "Total: " + str(item.selected_price * item.product_qty))
                pdf_canvas.drawString(text_x, y_position + image_height - 95, "Message: " + str(item.message))

                # Move y_position down for the next item row
                y_position -= item_row_height

            # Calculate x-coordinate for right alignment
            right_align_x = width - 290  # Adjust as needed for padding from the right edge

            # Draw total amount, date, and payment method on the right side
            y_coord = y_position + 50
            pdf_canvas.drawString(right_align_x, y_coord, "TOTAL AMOUNT:")
            pdf_canvas.drawString(right_align_x + 95, y_coord, f"Rs.{overall_total}")
        
            y_coord -= 20
            pdf_canvas.drawString(right_align_x, y_coord, "DATE:")
            pdf_canvas.drawString(right_align_x + 40, y_coord, f"{current_date}")
            
            y_coord -= 20
            pdf_canvas.drawString(right_align_x, y_coord, "PAYMENT METHOD:")
            pdf_canvas.drawString(right_align_x + 120, y_coord, "PAY ON DELIVERY")

            # Add "Thank You For Your Order" at the end with space above
            if y_position - 80 < 60:  # If there is not enough space for the thank you message
                pdf_canvas.showPage()
                y_position = height - 60  # Reset y_position

            thank_you_text = "Thank You For Your Order"
            pdf_canvas.setFont("Helvetica-BoldOblique", 18)
            text_width = pdf_canvas.stringWidth(thank_you_text, "Helvetica-BoldOblique", 18)
            x_position = (width - text_width) / 2
            y_position_thank_you = y_position - 80
            pdf_canvas.drawString(x_position, y_position_thank_you, thank_you_text)

            if contact_address_details:
                pdf_canvas.setFont("Helvetica", 12)
                pdf_canvas.drawString(x_position + 10, y_position_thank_you - 25, f"Mobile: +91 {contact_address_details.mobile}")

                # Break the address into two lines if it's too long
                max_line_length = 50  # Maximum length of characters per line
                address = contact_address_details.address

            if len(address) > max_line_length:
                # Find the last space within the limit to avoid breaking words
                split_index = address[:max_line_length].rfind(' ')
                address_line1 = address[:split_index]
                address_line2 = address[split_index + 1:]
                pdf_canvas.drawString(x_position + 10, y_position_thank_you - 40, address_line1)
                pdf_canvas.drawString(x_position + 10, y_position_thank_you - 55, address_line2)
            else:
                pdf_canvas.drawString(x_position + 10, y_position_thank_you - 40, address)

            pdf_canvas.showPage()
            pdf_canvas.save()

            order_items.delete()
            return response

        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            return HttpResponse('Failed to generate PDF. Please try again.', status=500)

    else:
        return HttpResponse('Method not allowed', status=405)
    

# @login_required(login_url="/userlogin")
# def generate_pdf(request,user_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
            
#             user_info = orders_item.objects.filter(user=request.user).last()
#             contact_address_details = contact_address.objects.last()

#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
#             current_date = datetime.now().strftime("%m/%d/%Y")

#             # Create the PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

#             # Create a canvas to draw on
#             pdf_canvas = canvas.Canvas(response, pagesize=letter)
#             width, height = letter

#             # Set background color
#             background_color = Color(242/255, 250/255, 215/255)  # Convert #fff3cd to RGB
#             pdf_canvas.setFillColor(background_color)
#             pdf_canvas.rect(0, 0, width, height, fill=1)
            
#             light_green = Color(153/255, 255/255, 153/255)  # RGB values for light green
#             pdf_canvas.setFillColor(light_green)
            
#             y_position = height - 100
#             logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')  # replace with your logo file path
#             logo_width, logo_height = 70, 90  # adjust the size of the logo
#             pdf_canvas.drawImage(logo_path, 50, y_position, logo_width, logo_height)

#             # Draw header text
#             pdf_canvas.setFillColorRGB(89/255, 116/255, 69/255)
#             pdf_canvas.setFont("Helvetica-BoldOblique", 24)  # bold, italic font
#             pdf_canvas.drawString(200, height - 70, "Rinku's Cakery Shop")
            
#             y_coord = height - 170 

#             # Set font and font size
#             pdf_canvas.setFont("Helvetica", 12)
#             pdf_canvas.setFillColorRGB(89/255, 116/255, 69/255)

#             # Draw invoice header
            
#             pdf_canvas.drawString(50, y_coord, "Email:")
#             pdf_canvas.drawString(150, y_coord, f"{user.email}")
            
#             y_coord -= 20
#             pdf_canvas.drawString(50, y_coord, "FIRST NAME:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.fname}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "LAST NAME:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.lname}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "PHONE:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.phone}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "ADDRESS:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.address}")

#             # Set initial y position for items
#             y_position = height - 390
#             item_row_height = 120  # Height of each item row including image and text

#             # Draw item table data
#             for item in order_items:
#                 # Calculate the x-coordinate for the image and text
#                 image_x = 130  # Position image 50 pixels from the left edge
#                 text_x = image_x + 180  # Position text to the right of the image

#                 # Define the image size
#                 image_width, image_height = 150, 100  # Adjust the size of the image

#                 # Define the border color and width
#                 border_color = Color(0, 0, 0)  # Black
#                 border_width = 3

#                 # Draw the rounded rectangle (border)
#                 pdf_canvas.setLineWidth(border_width)
#                 pdf_canvas.setStrokeColor(border_color)
#                 pdf_canvas.roundRect(image_x, y_position, image_width, image_height, 0, fill=0)

#                 # Draw image
#                 image_path = os.path.join(settings.MEDIA_ROOT, str(item.product.pimage))
#                 pdf_canvas.drawImage(image_path, image_x, y_position, image_width, image_height)

#                 # Draw text
#                 pdf_canvas.drawString(text_x, y_position + image_height - 20, item.product.pname)
#                 pdf_canvas.drawString(text_x, y_position + image_height - 40, "Quantity: " + str(item.product_qty))
#                 pdf_canvas.drawString(text_x, y_position + image_height - 60, "Price: " + str(item.selected_price))
#                 pdf_canvas.drawString(text_x, y_position + image_height - 80, "Total: " + str(item.selected_price * item.product_qty))
#                 pdf_canvas.drawString(text_x, y_position + image_height - 100, "Message: " + str(item.message))

#                 # Move y_position down for the next item row
#                 y_position -= item_row_height

#             # Calculate x-coordinate for right alignment
#             right_align_x = width - 200  # Adjust as needed for padding from the right edge

#             # Draw total amount, date, and payment method on the right side
#             y_coord = y_position + 50
#             pdf_canvas.drawString(right_align_x, y_coord, "TOTAL AMOUNT:")
#             pdf_canvas.drawString(right_align_x + 85, y_coord, f"Rs.{overall_total}")
        
#             y_coord -= 20
#             pdf_canvas.drawString(right_align_x, y_coord, "DATE:")
#             pdf_canvas.drawString(right_align_x + 35, y_coord, f"{current_date}")
            
#             y_coord -= 20
#             pdf_canvas.drawString(right_align_x, y_coord, "PAYMENT METHOD:")
#             pdf_canvas.drawString(right_align_x + 100, y_coord, "PAY ON DELIVERY")

#             # Add "Thank You For Your Order" at the end with space above
#             thank_you_text = "Thank You For Your Order"
#             pdf_canvas.setFont("Helvetica-BoldOblique", 18)
#             text_width = pdf_canvas.stringWidth(thank_you_text, "Helvetica-BoldOblique", 18)
#             x_position = (width - text_width) / 2
#             y_position_thank_you = y_position - 80
#             pdf_canvas.drawString(x_position, y_position_thank_you, thank_you_text)

#             if contact_address_details:
#                 pdf_canvas.setFont("Helvetica", 12)
#                 pdf_canvas.drawString(x_position + 10, y_position_thank_you - 25, f"Mobile: +91 {contact_address_details.mobile}")
#                 pdf_canvas.drawString(x_position + 10, y_position_thank_you - 40, f"Address: {contact_address_details.address}")

#             pdf_canvas.showPage()
#             pdf_canvas.save()

#             order_items.delete()
#             return response

#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {e}")
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)
    
    #         # Draw total amount
    #         y_position += 50
    #         y_coord = y_position
    #         pdf_canvas.drawString(50, y_coord, "TOTAL AMOUNT:")
    #         pdf_canvas.drawString(155, y_coord, f"Rs.{overall_total}")
        
    #         y_coord -= 20
    #         pdf_canvas.drawString(50, y_coord, "DATE:")
    #         pdf_canvas.drawString(95, y_coord, f"{current_date}")
            
    #         y_coord -= 20
    #         pdf_canvas.drawString(50, y_coord, "PAYMENT METHOD:")
    #         pdf_canvas.drawString(175, y_coord, "PAY ON DELIVERY")

    #         # Add "Thank You For Your Order" at the end with space above
    #         thank_you_text = "Thank You For Your Order"
    #         pdf_canvas.setFont("Helvetica-BoldOblique", 18)  # italic and bold font
    #         text_width = pdf_canvas.stringWidth(thank_you_text, "Helvetica-BoldOblique", 18)
    #         x_position = (width - text_width) / 2  # Calculate center position
    #         y_position_thank_you = y_position - 80  # Position the thank you text
    #         pdf_canvas.drawString(x_position, y_position_thank_you, thank_you_text)

    #         # Add mobile number and address below the thank you text
    #         if contact_address_details:
    #             pdf_canvas.setFont("Helvetica", 12)  # Reset font for additional text
    #             pdf_canvas.drawString(x_position + 10, y_position_thank_you - 25, f"Mobile: +91 {contact_address_details.mobile}")
    #             pdf_canvas.drawString(x_position + 10, y_position_thank_you - 40, f"Address: {contact_address_details.address}")

    #         # Finalize the PDF
    #         pdf_canvas.showPage()
    #         pdf_canvas.save()

    #         order_items.delete()
    #         return response

    #     except Exception as e:
    #         logger.error(f"Failed to generate PDF: {e}")
    #         return HttpResponse('Failed to generate PDF. Please try again.', status=500)

    # else:
    #     return HttpResponse('Method not allowed', status=405)

# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
#             user_info = orders_item.objects.filter(user=request.user).last()

#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
#             current_date = datetime.now().strftime("%m/%d/%Y")

#             # Create the PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

#             # Create a canvas to draw on
#             pdf_canvas = canvas.Canvas(response, pagesize=letter)
#             width, height = letter

#             light_green = Color(153/255, 255/255, 153/255)  # RGB values for light green
#             pdf_canvas.setFillColor(light_green)
            
#             y_position = height - 100
#             logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.jpeg')  # replace with your logo file path
#             logo_width, logo_height = 80, 80  # adjust the size of the logo
#             pdf_canvas.drawImage(logo_path, 50, y_position , logo_width, logo_height)

#             # Draw header text
            
#             # Set the text color to light green
#             pdf_canvas.setFillColorRGB(89/255, 116/255, 69/255)

#             # Draw the string
#             pdf_canvas.setFont("Helvetica-BoldOblique", 24)  # bold, italic font
#             pdf_canvas.drawString(200, height - 70, "Rinku's Cakery Shop")
            
#             y_coord = height - 150 

#             # Set font and font size
#             pdf_canvas.setFont("Helvetica", 12)
#             pdf_canvas.setFillColor(black)

#             # Draw invoice header
#             pdf_canvas.drawString(50, y_coord, "FIRST NAME:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.fname}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "LAST NAME:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.lname}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "PHONE:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.phone}")

#             y_coord -= 20  # move down to the next line
#             pdf_canvas.drawString(50, y_coord, "ADDRESS:")
#             pdf_canvas.drawString(150, y_coord, f"{user_info.address}")

#             y_position = height - 350
#             # Draw item table data
#             for item in order_items:
#             # Calculate the x-coordinate for the image and text
#                 image_x = width - 470  # position image 200 pixels from the right edge
#                 text_x = width - 270  # position text 150 pixels from the right edge

#                 # Define the image size
#                 image_width, image_height = 150, 100  # adjust the size of the image

#                 # Define the border color and width
#                 border_color = Color(0, 0, 0)  # black
#                 border_width = 3

#                 # Define the radius of the rounded corners
#                 radius = 0

#                 # Draw the rounded rectangle (border)
#                 pdf_canvas.setLineWidth(border_width)
#                 pdf_canvas.setStrokeColor(border_color)
#                 pdf_canvas.roundRect(image_x, y_position + 20, image_width, image_height, radius, fill=0)

#                 # Draw image
#                 image_path = str(item.product.pimage)
#                 pdf_canvas.drawImage(image_path, image_x, y_position + 20, image_width, image_height)

#                 # Draw text
#                 pdf_canvas.drawString(text_x, y_position + 95, item.product.pname)
#                 pdf_canvas.drawString(text_x, y_position + 75, "Quantity: " + str(item.product_qty))
#                 pdf_canvas.drawString(text_x, y_position + 55, "Price: " + str(item.selected_price))
#                 pdf_canvas.drawString(text_x, y_position + 35, "Total: " + str(item.selected_price * item.product_qty))

#                 y_position -= 90  # adjust the row height to accommodate the image

#             # Draw total amount
#             y_coord = 100
#             pdf_canvas.drawString(50, y_coord, "TOTAL AMOUNT:")
#             pdf_canvas.drawString(155, y_coord, f"₹{overall_total}")
        
#             y_coord -= 20
#             pdf_canvas.drawString(50, y_coord, "DATE:")
#             pdf_canvas.drawString(95, y_coord, f"{current_date}")
            
#             y_coord -= 20
             
#             pdf_canvas.drawString(50, y_coord, "PAYMENT METHOD:")
#             pdf_canvas.drawString(175, y_coord, "PAY ON DELIVERY")

#             # Finalize the PDF
#             pdf_canvas.showPage()
#             pdf_canvas.save()

#             # order_items.delete()
#             return response

            

#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {e}")
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)

# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
#             user_info = orders_item.objects.filter(user=request.user).last()

#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
#             current_date = datetime.now().strftime("%m/%d/%Y")

#             # Create the PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

#             # Create a canvas to draw on
#             pdf_canvas = canvas.Canvas(response, pagesize=letter)
#             width, height = letter

#             pdf_canvas.setFillColorRGB(231, 240, 220)  # Light gray background
#             pdf_canvas.rect(0, 0, width, height, fill=1)
            
#             logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')  # replace with your logo file path
#             logo_width, logo_height = 200, 50  # adjust the size of the logo
#             pdf_canvas.drawImage(logo_path, 50, height - 70, width=logo_width, height=logo_height)

#             # Draw header text
#             pdf_canvas.setFont("Helvetica-BoldOblique", 24)  # bold, italic font
#             pdf_canvas.setFillColorRGB(63, 89, 30)  # black text color
#             pdf_canvas.drawString(170, height - 60, "Rinku's Cakery Shop")

#             # Set font and font size
#             pdf_canvas.setFont("Helvetica", 12)

#             # Draw invoice header
#             pdf_canvas.drawString(50, height - 50, "FIRST NAME:")
#             pdf_canvas.drawString(150, height - 50, "LAST NAME:")
#             pdf_canvas.drawString(250, height - 50, "PHONE:")
#             pdf_canvas.drawString(350, height - 50, "ADDRESS:")
#             pdf_canvas.drawString(50, height - 70, f"{user_info.fname}")
#             pdf_canvas.drawString(150, height - 70, f"{user_info.lname}")
#             pdf_canvas.drawString(250, height - 70, f"{user_info.phone}")
#             pdf_canvas.drawString(350, height - 70, f"{user_info.address}")

#             # Draw item table header
#             pdf_canvas.drawString(50, height - 150, "ITEM DESCRIPTION")
#             pdf_canvas.drawString(200, height - 150, "QTY")
#             pdf_canvas.drawString(250, height - 150, "PRICE")
#             pdf_canvas.drawString(300, height - 150, "TOTAL")

#             # Draw item table data
#             y_position = height - 170
#             for item in order_items:
#                 pdf_canvas.drawString(50, y_position, item.product.pname)
#                 pdf_canvas.drawString(200, y_position, str(item.product_qty))
#                 pdf_canvas.drawString(250, y_position, str(item.selected_price))
#                 pdf_canvas.drawString(300, y_position, str(item.selected_price * item.product_qty))
#                 y_position -= 20

#             # Draw total amount
#             pdf_canvas.drawString(250, y_position, "TOTAL AMOUNT:")
#             pdf_canvas.drawString(300, y_position, f"${overall_total}")

#             # Finalize the PDF
#             pdf_canvas.showPage()
#             pdf_canvas.save()

#             return response

#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {e}")
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)

# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
#             user_info = orders_item.objects.filter(user=request.user).last()

#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
#             current_date = datetime.now().strftime("%Y-%m-%d")

#             # Create the PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

#             # Create a canvas to draw on
#             pdf_canvas = canvas.Canvas(response, pagesize=letter)
#             width, height = letter

#             # Draw background image
#             background_path = os.path.join(settings.MEDIA_ROOT, 'bill_bg.jpg')
#             if os.path.exists(background_path):
#                 pdf_canvas.drawImage(background_path, 0, 0, width=width, height=height)

#             styles = getSampleStyleSheet()
#             text_style = styles['Normal']

#             # Draw user information at the top
#             if user_info:
#                 user_info_text = (
#                     f"First Name: {user_info.fname}\n"
#                     f"Last Name: {user_info.lname}\n"
#                     f"Phone Number: {user_info.phone}\n"
#                     f"Address: {user_info.address}\n"
#                 )
#                 pdf_canvas.drawString(50, height - 100, user_info_text)

#             # Define positions
#             x_image_start = 50
#             x_text_start = 210
#             y_position = height - 200

#             # Add the cake background image
#             cake_background_path = os.path.join(settings.MEDIA_ROOT, 'bill_bg.jpg')
#             if os.path.exists(cake_background_path):
#                 pdf_canvas.drawImage(cake_background_path, x_image_start, y_position, width=400, height=200)

#             for item in order_items:
#                 image_path = os.path.join(settings.MEDIA_ROOT, str(item.product.pimage))
#                 if os.path.exists(image_path):
#                     pdf_canvas.drawImage(image_path, x_image_start, y_position, width=150, height=150)

#                 product_info = (
#                     f"Product Name: {item.product.pname}\n"
#                     f"Price: {item.selected_price}\n"
#                     f"Weight: {item.selected_weight}\n"
#                     f"Quantity: {item.product_qty}\n"
#                     f"Total Price: {item.selected_price * item.product_qty}\n"
#                 )
#                 text_object = pdf_canvas.beginText(x_text_start, y_position + 150)
#                 text_object.setTextOrigin(x_text_start, y_position + 150)
#                 text_object.setFont("Helvetica", 10)
#                 text_object.textLines(product_info)
#                 pdf_canvas.drawText(text_object)
                
#                 y_position -= 200  # Adjust for image height + padding

#             # Draw footer with date, overall total, and payment method
#             footer_text = (
#                 f"Date: {current_date}\n"
#                 f"Overall Total: Rs. {overall_total}\n"
#                 f"Payment Method: Pay On Delivery\n"
#             )
#             footer_object = pdf_canvas.beginText(50, 100)
#             footer_object.setTextOrigin(50, 100)
#             footer_object.setFont("Helvetica", 12)
#             footer_object.textLines(footer_text)
#             pdf_canvas.drawText(footer_object)

#             # Finalize the PDF
#             pdf_canvas.showPage()
#             pdf_canvas.save()

#             return response

#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {e}")
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)



# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
#             user_info = orders_item.objects.filter(user=request.user).last()

#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
#             current_date = datetime.now().strftime("%Y-%m-%d")

#             # Create the PDF document
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="cake_order_summary.pdf"'

#             # Create a canvas to draw on
#             pdf_canvas = canvas.Canvas(response, pagesize=letter)
#             width, height = letter

#             # Draw background image
#             background_path = os.path.join(settings.MEDIA_ROOT, 'bill_bg.jpg')
#             if os.path.exists(background_path):
#                 pdf_canvas.drawImage(background_path, 0, 0, width=width, height=height)

#             styles = getSampleStyleSheet()
#             text_style = styles['Normal']

#             # Draw user information at the top
#             if user_info:
#                 user_info_text = (
#                     f"First Name: {user_info.fname}\n"
#                     f"Last Name: {user_info.lname}\n"
#                     f"Phone Number: {user_info.phone}\n"
#                     f"Address: {user_info.address}\n"
#                 )
#                 pdf_canvas.drawString(50, height - 100, user_info_text)

#             # Define positions
#             x_image_start = 50
#             x_text_start = 210
#             y_position = height - 200

#             for item in order_items:
#                 image_path = os.path.join(settings.MEDIA_ROOT, str(item.product.pimage))
#                 if os.path.exists(image_path):
#                     pdf_canvas.drawImage(image_path, x_image_start, y_position, width=150, height=150)

#                 product_info = (
#                     f"Product Name: {item.product.pname}\n"
#                     f"Price: {item.selected_price}\n"
#                     f"Weight: {item.selected_weight}\n"
#                     f"Quantity: {item.product_qty}\n"
#                     f"Total Price: {item.selected_price * item.product_qty}\n"
#                 )
#                 text_object = pdf_canvas.beginText(x_text_start, y_position + 150)
#                 text_object.setTextOrigin(x_text_start, y_position + 150)
#                 text_object.setFont("Helvetica", 10)
#                 text_object.textLines(product_info)
#                 pdf_canvas.drawText(text_object)
                
#                 y_position -= 200  # Adjust for image height + padding

#             # Draw footer with date, overall total, and payment method
#             footer_text = (
#                 f"Date: {current_date}\n"
#                 f"Overall Total: Rs. {overall_total}\n"
#                 f"Payment Method: Pay On Delivery\n"
#             )
#             footer_object = pdf_canvas.beginText(50, 100)
#             footer_object.setTextOrigin(50, 100)
#             footer_object.setFont("Helvetica", 12)
#             footer_object.textLines(footer_text)
#             pdf_canvas.drawText(footer_object)

#             # Finalize the PDF
#             pdf_canvas.showPage()
#             pdf_canvas.save()

#             return response

#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {e}")
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)

# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = Cart_Data.objects.filter(user=request.user)
#             user_info = orders_item.objects.filter(user=request.user).last()
#              # Create a PDF object
#             # Calculate overall total
#             overall_total = float(sum(item.selected_price * item.product_qty for item in order_items))
            
            
#             # Current date
#             current_date = datetime.now().strftime("%Y-%m-%d")

#             # Define the filename and path for the PDF
#             filename = os.path.join(settings.MEDIA_ROOT, 'cake_order_summary.pdf')

#             # Create the PDF document
#             doc = SimpleDocTemplate(filename, pagesize=letter)
#             elements = []

#             logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')  # Replace 'your_logo.png' with your actual logo filename
#             if os.path.exists(logo_path):
#                 elements.append(Paragraph("Rinku's Cakery Shop"))
           
#             if user_info:
#                 user_info_text = (
#                     f"First Name: {user_info.fname}\n"
#                     f"Last Name: {user_info.lname}\n"
#                     f"Phone Number: {user_info.phone}\n"
#                     f"Address: {user_info.address}\n"
#                 )
#                 elements.append(Paragraph(user_info_text))
#             # Add content to the PDF
#             data = [
#                 ['Product Image','Product Name', 'Price', 'Weight', 'Quantity', 'Total Price']
#             ]
#             for item in order_items:
#                 # Assuming item.product.pimage is the path to the image file
#                 image_path = os.path.join(settings.MEDIA_ROOT,str(item.product.pimage))
#                 if os.path.exists(image_path):
#                     img = Image(image_path)
#                     img.drawHeight = 100  # Adjust image height as needed
#                     img.drawWidth = 100    # Adjust image width as needed
#                 else:
#                     img = ""

#                 total_price = item.selected_price * item.product_qty
#                 data.append([
#                     img,
#                     item.product.pname,
#                     item.selected_price,
#                     item.selected_price,
#                     item.product_qty,
#                     total_price
#                 ])

#             # Create a Table object
#             table = Table(data)

#             # Add style to the table
#             style = TableStyle([
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#             ])

#             # Apply style to the table
#             table.setStyle(style)

#             # Add the table to the elements list of the PDF
#             elements.append(table)

#             # Add other order details as separate elements
#             elements.append(Paragraph(f"Date: {current_date}"))
#             elements.append(Paragraph(f"Overall Total: Rs. {overall_total}"))
#             elements.append(Paragraph("Payment Method: Pay On Delivery"))

#             # Build PDF document
#             doc.build(elements)

#             # Open the generated PDF file
#             with open(filename, 'rb') as pdf_file:
#                 response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#                 response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
#                 return response

#         except Exception as e:
#             # Log the error for debugging purposes
#             print(str(e))
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)

# @login_required(login_url="/userlogin")
# def generate_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve user's order details
#             order_items = orders_item.objects.filter(user=request.user)

#             # Calculate overall total
#             overall_total = sum(item.total_price for item in order_items)

#             # Current date
#             current_date = datetime.now().strftime("%Y-%m-%d")

#             # Define the filename and path for the PDF
#             filename = os.path.join(settings.MEDIA_ROOT, 'order_summary.pdf')

#             # Create the PDF document
#             doc = SimpleDocTemplate(filename, pagesize=letter)
#             elements = []

#             # Add content to the PDF
#             data = [
#                 ['Product Name', 'Price', 'Weight', 'Quantity', 'Total Price']
#             ]
#             for item in order_items:
#                 data.append([
#                     item.product.pname,
#                     f"Rs.{item.price}",  # Assuming item.price is an integer
#                     item.weight,
#                     item.quantity,
#                     f"Rs.{item.total_price}"  # Assuming item.total_price is an integer
#                 ])

#             # Create a Table object
#             table = Table(data)

#             # Add style to the table
#             style = TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#             ])
#             table.setStyle(style)

#             # Add the table to the elements list of the PDF
#             elements.append(table)

#             # Add other order details
#             elements.append(f"Date: {current_date}")
#             elements.append(f"Total: Rs.{overall_total}")
#             elements.append(f"Payment Method: Pay On Delivery")

#             # Build PDF document
#             doc.build(elements)

#             # Open the generated PDF file
#             with open(filename, 'rb') as pdf_file:
#                 response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#                 response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename)
#                 return response

#         except Exception as e:
#             # Log the error for debugging purposes
#             print(str(e))
#             return HttpResponse('Failed to generate PDF. Please try again.', status=500)

#     else:
#         return HttpResponse('Method not allowed', status=405)

# def generate_pdf(request):
#     if request.method == 'POST':
#         # Retrieve user's order details
#         order_items = order_items.objects.filter(user=request.user)

#         # Calculate overall total
#         overall_total = sum(item.total_price for item in order_items)

#         # Current date
#         current_date = datetime.now().strftime("%Y-%m-%d")

#         # Define the filename and path for the PDF
#         filename = os.path.join(settings.BASE_DIR, 'order_summary.pdf')

#         # Create the PDF document
#         doc = SimpleDocTemplate(filename, pagesize=letter)
#         elements = []

#         # Add content to the PDF
#         data = [
#             ['Product Name', 'Price', 'Weight', 'Quantity', 'Total Price']
#         ]
#         for item in order_items:
#             data.append([
#                 item.product_name,
#                 f"Rs.{item.price}",
#                 item.weight,
#                 item.quantity,
#                 f"Rs.{item.total_price}"
#             ])

#         # Create a Table object
#         table = Table(data)

#         # Add style to the table
#         style = TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#         ])
#         table.setStyle(style)

#         # Add the table to the elements list of the PDF
#         elements.append(table)

#         # Add other order details
#         elements.append(f"Date: {current_date}")
#         elements.append(f"Total: Rs.{overall_total}")
#         elements.append(f"Payment Method: Pay On Delivery")

#         # Build PDF document
#         doc.build(elements)

#         # Open the generated PDF file
#         with open(filename, 'rb') as pdf_file:
#             response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename)
#             return response

#     else:
#         return HttpResponse('Method not allowed', status=405)

# def generate_pdf(request):
#     if request.method == 'POST':
#         # Retrieve user's order details
#         order_items = order_items.objects.filter(user=request.user)

#         # Calculate overall total
#         overall_total = sum(item.total_price for item in order_items)

#         # Current date
#         current_date = datetime.now().strftime("%Y-%m-%d")

#         # Generate PDF
#         pdf_filename = create_pdf(order_items, overall_total, current_date)

#         # Clear the user's cart (assuming you have a method for this in your cart logic)
#         # cart.clear()  # Uncomment and replace with actual logic to clear the cart

#         # Open the generated PDF file
#         file_path = os.path.join(settings.BASE_DIR, pdf_filename)
#         with open(file_path, 'rb') as pdf_file:
#             response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
#             return response

#     else:
#         return HttpResponse('Method not allowed', status=405)

# def create_pdf(order_items, overall_total, current_date):
#     # Define the filename and path
#     filename = os.path.join(settings.BASE_DIR, 'order_summary.pdf')

#     # Create the PDF document
#     doc = SimpleDocTemplate(filename, pagesize=letter)
#     elements = []

#     # Add content to the PDF
#     data = [
#         ['Product Name', 'Price', 'Weight', 'Quantity', 'Total Price']
#     ]
#     for item in order_items:
#         data.append([
#             item.product_name,
#             f"Rs.{item.price}",
#             item.weight,
#             item.quantity,
#             f"Rs.{item.total_price}"
#         ])

#     # Create a Table object
#     table = Table(data)

#     # Add style to the table
#     style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#     ])
#     table.setStyle(style)

#     # Add the table to the elements list of the PDF
#     elements.append(table)

#     # Add other order details
#     elements.append(f"Date: {current_date}")
#     elements.append(f"Total: Rs.{overall_total}")
#     elements.append(f"Payment Method: Pay On Delivery")

#     # Build PDF document
#     doc.build(elements)

#     return filename

# def generate_pdf(request):
#     if request.method == 'POST':
#         # Retrieve user and order details
#         user_details = get_object_or_404(orders_item, user=request.user)

#         # Calculate overall total
#         overall_total = sum(item.total_price for item in user_details)

#         # Current date
#         current_date = datetime.now().strftime("%Y-%m-%d")

#         # Generate PDF
#         pdf_filename = generate_pdf(user_details, overall_total, current_date)

#         # Return JSON response with PDF filename
#         return HttpResponse(json.dumps({'pdf_filename': pdf_filename}), content_type='application/json')
#     else:
#         return HttpResponse('Method not allowed', status=405)

# def generate_pdf(order_items, overall_total, current_date):
#     from reportlab.lib.pagesizes import letter
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#     from reportlab.lib import colors

#     filename = "order_summary.pdf"

#     # Create the PDF document
#     doc = SimpleDocTemplate(filename, pagesize=letter)
#     elements = []

#     # Add content to the PDF
#     data = [
#         ['Product Name', 'Price', 'Weight', 'Quantity', 'Total Price']
#     ]
#     for item in order_items:
#         data.append([
#             item.product.pname,
#             f"Rs.{item.price}",
#             item.weight,
#             item.quantity,
#             f"Rs.{item.total_price}"
#         ])

#     # Create a Table object
#     table = Table(data)

#     # Add style to the table
#     style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#     ])
#     table.setStyle(style)

#     # Add the table to the elements list of the PDF
#     elements.append(table)

#     # Add other order details
#     elements.append(f"Date: {current_date}")
#     elements.append(f"Total: Rs.{overall_total}")
#     elements.append(f"Payment Method: Pay On Delivery")

#     # Build PDF document
#     doc.build(elements)

#     return filename

# def download_pdf(request):
#     filename = request.GET.get('filename')
#     file_path = os.path.join(settings.BASE_DIR, filename)

#     with open(file_path, 'rb') as pdf_file:
#         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
#         return response

# def generate_pdf(request, user_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     orders = orders_item.objects.filter(user=user)
#     overall_total = sum(item.price for item in orders)

#     # Create a file-like buffer to receive PDF data
#     buffer = BytesIO()

#     # Create a canvas object that will be used to generate PDF
#     p = canvas.Canvas(buffer, pagesize=letter)

#     # Start PDF generation
#     y_position = 750
#     p.drawString(100, y_position, f"Orders for {user.username}")
#     y_position -= 20

#     # Loop through orders and write details to PDF
#     for order in orders:
#         p.drawString(100, y_position, f"Order ID: {order.id}")
#         y_position -= 20
#         p.drawString(100, y_position, f"Customer Information:")
#         y_position -= 15
#         p.drawString(120, y_position, f"Name: {order.fname} {order.lname}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Email: {order.email}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Phone: {order.phone}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Address: {order.address}")
#         y_position -= 20
#         p.drawString(100, y_position, f"Product Information:")
#         y_position -= 15
#         p.drawString(120, y_position, f"Product Name: {order.product.pname}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Product Price: ₹{order.price}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Quantity: {order.quantity}")
#         y_position -= 15
#         p.drawString(120, y_position, f"Weight: {order.weight}")
#         y_position -= 20

#     # Overall Total
#     p.drawString(100, y_position, f"Overall Total: ₹{overall_total}")

#     # End PDF generation
#     p.showPage()
#     p.save()

#     # Get the value of the BytesIO buffer and write it to the response
#     pdf = buffer.getvalue()
#     buffer.close()

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="user_orders_{user.id}.pdf"'
#     response.write(pdf)

#     return response


# def checkout_page(request,user_id):
#     if request.method == "POST":
#         cd = checkout_data()
#         cd.user = request.user
#         cd.fname = request.POST.get('fname')
#         cd.lname = request.POST.get('fname')
#         cd.email = request.POST.get('email')
#         cd.phone = request.POST.get('phone')
#         cd.delhivery_address = request.POST.get('delhivery_address')
#         cd.delhivery_address = request.POST.get('delhivery_address')
        
#         cart = Cart_Data.objects.filter(user=request.user)
#         cart_total_price=0
#         for item in cart:
#             cart_total_price = sum(item.total_price for item in cart)
#             cart_total_price
#         cd.cart_total_price = cart_total_price
#         trackno =str(random.randint(111111,999999))
#         while checkout_data.objects.filter(tracking_no=trackno) is None:
#             trackno =str(random.randint(111111,999999))
#         cd.tracking_no = trackno
#         cd.save()
        
#         cditems = Cart_Data.objects.filter(user=request.user)
#         for item in cditems:
#             orderitem.objects.create(
#                 order = cd,
#                 product = item.product,
#                 quantity = item.product_qty,
#                 price = item.selected_price,
#             )
            
#             checkoutproduct = Product.objects.filter(id=item.product_id).first()
#             checkoutproduct.quantity = checkoutproduct.quantity - item.product_qty
#             checkoutproduct.save()
#         Cart_Data.objects.filter(user=request.user).delete()
#         messages.success(request,"your order placed successfully")
#     return redirect('index')
#     return render(request,"checkout.html")


# def checkout_page(request, user_id):
#     user_profile = get_object_or_404(UserProfile, id=user_id)
#     cart_items = Cart_Data.objects.filter(user=user_profile)
#     overall_total = sum(item.selected_price for item in cart_items)
#     is_empty_cart = not cart_items.exists()
    
    
#     if request.method == 'POST':
    
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         delhivery_address = request.POST['delhivery_address']

#          # Calculate total_price
            
#         for cart_item in cart_items:
#             checkoutdata.objects.create(
#                 user=user_profile,
#                 product=cart_item.product,
#                 cart=cart_item,
#                 fname=fname,
#                 lname=lname,
#                 email=email,
#                 phone=phone,
#                 delhivery_address=delhivery_address,
#                 total_price=cart_item.selected_price
#             )
#             # Optionally, delete cart_items after checkout
#         Cart_Data.objects.filter(user=user_profile).delete()
        
#         # Redirect to order confirmation page or display a success message
#         # return JsonResponse({"status": "success", "message": "Checkout successful."})
#         return redirect('index')

#         # except user_profile.DoesNotExist:
#         #     return JsonResponse({"status": "error", "message": "User not found. Please check the user ID."}, status=404)
#         # except Exception as e:
#         #     return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"}, status=500)

#         # else:
#         #     return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)    
       

#     else:
#         form = checkoutdata()
        
#     return render(request, 'user/checkout.html', {
#         'form': form,
#         'cart_items': cart_items,
#         'overall_total': overall_total,
#         'is_empty_cart': is_empty_cart
#     })



# def checkout_page(request,user_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     cart_items = Cart_Data.objects.filter(user=user)
#     overall_total = sum(item.selected_price * item.product_qty for item in cart_items)
#     is_empty_cart = not cart_items.exists()
    
#     if request.method == 'POST':
#         form = checkout_data(request.POST)
#         if form.is_valid():
#             cd = form.save(commit=False)
#             cd.user = user
#             cd.id = Cart_Data.objects.get(user=user)
#             cd.save()
#             cart_items.delete()
#             return redirect('/home')
        
#     else:
#         form = checkout_data()   
        
#     return render(request, 'user/checkout.html',{'form': form,'cart_items': cart_items,'overall_total': overall_total,'is_empty_cart': is_empty_cart})

# def checkout_page(request, user_id):
#     user_profile = get_object_or_404(UserProfile, id=user_id)
#     cart_items = Cart_Data.objects.filter(user=user_profile)
#     overall_total = sum(item.selected_price * item.product_qty for item in cart_items)
#     is_empty_cart = not cart_items.exists()

#     if request.method == 'POST':
#         form = checkout_data(request.POST)

#         if form.is_valid():
#             checkout_instance = form.save(commit=False)
#             checkout_instance.user = user_profile
#             checkout_instance.save()

#             # Deleting all items in the cart after successful checkout
#             cart_items.delete()

#             return redirect('/home')
#         else:
#             print("Form is not valid")  # Debugging line
#             print(form.errors)  # Debugging line
#     else:
#         form = checkout_data()

#     return render(request, 'user/checkout.html', {
#         'form': form,
#         'cart_items': cart_items,
#         'overall_total': overall_total,
#         'is_empty_cart': is_empty_cart
#     })

# def checkout_page(request, user_id):
#     user_profile = get_object_or_404(UserProfile, id=user_id)
#     cart_items = Cart_Data.objects.filter(user=user_profile)
#     overall_total = sum(item.selected_price * item.product_qty for item in cart_items)
#     is_empty_cart = not cart_items.exists()

#     if request.method == 'POST':
#         form = checkout_data(request.POST)

#         if form.is_valid():
#             if cart_items.exists():

#                 # Create Checkout instances for each cart item
#                 for cart_item in cart_items:
#                     form=checkout.objects.create(
#                         user=user_profile,
#                         product=cart_item.product,
#                         cart=cart_item,
#                         name=request.POST['name'],
#                         email=request.POST['email'],
#                         phone=request.POST['phone'],
#                         delhivery_address=request.POST['delhivery_address'],
#                         office_address=request.POST['office_address'],
#                         home_address=request.POST['home_address'],
#                     )
#                 form.save()
                    
#                 print("Checkout data saved successfully.")
#                 print(f"Number of items deleted from cart: {len(cart_items)}")

#                 cart_items.delete()
            
#                 # Debugging print statements
                
#                 return redirect('index')
#             else:
#                 print("No cart items found for the user.")
#         else:
#             print("Form is not valid")
#             print(form.errors)
#     else:
#         form = checkout_data()

#     return render(request, 'user/checkout.html', {'form': form,'cart_items': cart_items,'overall_total': overall_total,'is_empty_cart': is_empty_cart})
    
    


# cd = checkout_data()

        # if request.method == "POST":
        #     cdform = checkout_data(request.POST,request.FILES)
        # if cdform.is_valid():
        #     cd = cdform.save(commit=False)
        #     cd.user = request.user  # Access UserProfile through the related name 'profile'
            
        #     product_id = request.POST.get('product_id')
        #     if not product_id:
        #         return render(request, 'user/checkout.html', {'cdform': cdform, 'products': Product.objects.all(), 'error': 'Product ID is missing'})

        #     try:
        #         product = Product.objects.get(id=product_id)
        #     except Product.DoesNotExist:
        #         return render(request, 'user/checkout.html', {'cdform': cdform, 'products': Product.objects.all(), 'error': 'Product does not exist'})
            
        #     cd.product = product
        #     cd.cart = Cart_Data.objects.get(user=request.user)  # Adjust if needed
        #     cd.save()
        #     return redirect('/home')
        # products = Product.objects.all()

        # cd.user = request.user  # assuming UserProfile is linked to User
        # cd.product = Product.objects.get(id=request.POST.get('product_id'))
        # cd.cart = Cart_Data.objects.get(user=request.user)  # example, adjust as needed
        # cd.save()
        # return redirect("/view_checkoutdata")
        
        
        
