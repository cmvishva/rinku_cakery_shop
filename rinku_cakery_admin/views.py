import random
from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import get_object_or_404, render,redirect
from rinku_cakery_admin.models import *
from rinku_cakery_user.models import *
# Create your views here.
from django.contrib.admin.models import LogEntry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordChangeView

def adminlogin(request):
    msg=''
    
    if request.method == 'POST':
        adminusername = request.POST['adminusername']
        adminpassword = request.POST['adminpassword']

        obj = admindata.objects.filter(adminusername = adminusername,adminpassword = adminpassword)
        if obj.count()>0:
            data = obj.get()
            request.session['admin_username'] = data.adminusername
            return redirect('/dashboard')
        else:
            messages.error(request, "Please enter a valid username or password")
    
    if 'admin_username' in request.session:
        return redirect('/dashboard')

    return render(request,"Authentication/AdminLogin.html")

def adminregister(request):
    if request.method == 'POST':
        
        adminusername = request.POST['adminusername']
        adminpassword = request.POST['adminpassword']
        obj = admindata(
           
            adminusername = adminusername,
            adminpassword = adminpassword,
        )
        obj.save()  
        return redirect("/adminlogin")

    return render(request,"Authentication/AdminRegister.html")

def admin_logout(request):
    logout(request)
    # Optionally, perform additional actions here
    return redirect('/adminlogin')


@login_required
def generate_otp():
    return str(random.randint(100000, 999999))

@login_required
def request_otp_view(request):
    otp = generate_otp()
    request.session['otp'] = otp
    # Send the OTP to a static email address
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'from@example.com',
        ['vishva.cminfotech@gmail.com'],
        fail_silently=False,
    )
    messages.success(request, 'OTP has been sent to your email.')
    return redirect('verify_otp')

@login_required
def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()  # Ensure input is a string
        session_otp = str(request.session.get('otp', '')).strip()  # Ensure session OTP is a string
        print(f"Entered OTP (after strip): '{entered_otp}'")  # Debugging line
        print(f"Session OTP (after strip): '{session_otp}'")  # Debugging line
        if entered_otp == session_otp:
            del request.session['otp']
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'Authentication/verify_otp.html')

def admin_change_password(request):
    if 'admin_username' in request.session:
        admin_username = request.session['admin_username']
        admin_data = admindata.objects.get(adminusername=admin_username)

        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            # Validate old password
            if not check_password(old_password, admin_data.adminpassword):
                messages.error(request, 'Incorrect current password.')
                return redirect('/admin_change_password')

            # Validate new passwords match
            if new_password1 != new_password2:
                messages.error(request, 'The new passwords do not match.')
                return redirect('/admin_change_password')

            # Update password in the admin_data object
            admin_data.adminpassword = make_password(new_password1)
            admin_data.save()

            messages.success(request, 'Your password was successfully updated!')
            return redirect('/adminlogin')  # Redirect to the admin login page or any other page
        else:
            return render(request, 'Authentication/change_password.html')
    else:
        return redirect('/adminlogin')

from django.contrib.auth.decorators import login_required

def dashboard(request):
    if 'admin_username' in request.session:
        return render(request, "dashboard.html")
    else:
        return redirect('/adminlogin')

def add_mainmenu(request):
    if 'admin_username' in request.session:
        if request.method == "POST":
            menuname = request.POST['menuname']
            menuurl = request.POST['menuurl']
            
            obj = Main_menu(
                menuname = menuname,
                menuurl = menuurl,
            )
            obj.save()
            return redirect('/view_main_menu')
    else:
        return redirect('/adminlogin')
    return render(request,"add-mainmenu.html")

def view_mainmenu(request):
    if 'admin_username' in request.session:
        viewmenu = Main_menu.objects.all()
    else:
        return redirect('/adminlogin')

    return render(request,"view-mainmenu.html",{"viewmenu":viewmenu})
    
def delete_mainmenu(request,id):
    if 'admin_username' in request.session:
    # if 'adminemail' in request.session:        
        delmenu = Main_menu.objects.get(id=id).delete()
        return redirect('/view_main_menu')
        # else:
        #     return redirect('/login_admin/')
        return render(request,"add-mainmenu.html")
    else:
        return redirect('/adminlogin')


def update_mainmenu(request,id):
    if 'admin_username' in request.session:
        umenu = Main_menu.objects.get(id=id)
        if request.method == "POST":
            menuname = request.POST['menuname']
            menuurl = request.POST['menuurl']
            
            umenu.menuname=menuname
            umenu.menuurl=menuurl
            umenu.save()
            return redirect('/view_main_menu')
    else:
        return redirect('/adminlogin')

    return render(request,"add-mainmenu.html",{'umenu':umenu})


def addslider(request):
    if 'admin_username' in request.session:
        # if 'userid' in request.session:
        sd = Sliderdata()

        if request.method == "POST":
            sd = Sliderdata(request.POST,request.FILES)
            sd.save()
            return redirect("/view_slider")
        # else:
        #     return redirect("/login/")
    else:
        return redirect('/adminlogin')

    return render(request,"Home-Page/add-slider.html",{"sd":sd})


def viewslider(request):
    if 'admin_username' in request.session:
        # if 'userid' in request.session:   
        slider = Sliders.objects.all()    
    else:
        return redirect('/adminlogin')
    
    return render(request,"Home-Page/view-slider.html",{"slider":slider})

def deleteslider(request,id):
    if 'admin_username' in request.session:
        # if 'adminemail' in request.session:        
        delslider = Sliders.objects.get(id=id).delete()
        return redirect("/view_slider")
    else:
        return redirect('/adminlogin')


def updateslider(request,id):
    if 'admin_username' in request.session:
        usd = get_object_or_404(Sliders,id=id)
        if request.method == "POST":
            sd = Sliderdata(request.POST,request.FILES,instance=usd)
            if sd.is_valid():
                sd.save()
                return redirect('/view_slider')
            else:
                print(sd.errors)
                return render(request,"Home-Page/add-slider.html",{"sd":sd})
        else:
            sd = Sliderdata(instance = usd,initial={'simage': usd.simage, 'sname': usd.sname, 'sdesc': usd.sdesc})
        return render(request,"Home-Page/add-slider.html",{"sd":sd})

# def addproduct(request):
#     return render(request,"admin/add-product.html")


    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ About Page   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def add_about_header_img(request):
    if 'admin_username' in request.session:
        # if 'userid' in request.session:
        ahi = about_header_data()

        if request.method == "POST":
            ahi = about_header_data(request.POST,request.FILES)
            ahi.save()
            return redirect("/view_about_header_img")
    else:
        return redirect('/adminlogin')

    return render(request,"About-Page/add-about_header_image.html",{"ahi":ahi})


def view_about_header_img(request):
    if 'admin_username' in request.session:   
        about_header_img = aboutheader.objects.all()    
    else:
        return redirect('/adminlogin')
  
    return render(request,"About-Page/view-about_header_image.html",{"about_header_img":about_header_img})

def delete_about_header_img(request,id):
    if 'admin_username' in request.session:        
        delabout_headerimg = aboutheader.objects.get(id=id).delete()
        return redirect("/view_about_header_img")
    else:
        return redirect('/adminlogin')

def update_about_header_img(request,id):
    uahi = get_object_or_404(aboutheader,id=id)
    if request.method == "POST":
        ahi = about_header_data(request.POST,request.FILES,instance=uahi)
        if ahi.is_valid():
            ahi.save()
            return redirect('/view_about_header_img')
        else:
            print(ahi.errors)
            return render(request,"About-Page/add-about_header_image.html",{"ahi":ahi})
    else:
        ahi = about_header_data(instance = uahi,initial={'about_header_text': uahi.about_header_text,"about_header_img":uahi.about_header_img})
    return render(request,"About-Page/add-about_header_image.html",{"ahi":ahi})

# =============================================== About sec 1 ==================================================================

def add_about_sec1(request):
    if 'admin_username' in request.session:
        as1 = About_sec1_data()

        if request.method == "POST":
            as1 = About_sec1_data(request.POST,request.FILES)
            as1.save()
            return redirect("/view_about_sec1")
    else:
        return redirect('/adminlogin')
    return render(request,"About-Page/add-about_sec1.html",{"as1":as1})


def view_about_sec1(request):
    if 'admin_username' in request.session:   
        about_sec1 = Aboutsec1.objects.all()    
    else:
        return redirect('/adminlogin')
    return render(request,"About-Page/view-about_sec1.html",{"about_sec1":about_sec1})


def delete_about_sec1(request,id):
    if 'admin_username' in request.session:        
        delas1 = Aboutsec1.objects.get(id=id).delete()
        return redirect("/view_about_sec1")
    else:
        return redirect('/adminlogin')


def update_about_sec1(request,id):
    uas1 = get_object_or_404(Aboutsec1,id=id)
    if request.method == "POST":
        as1 = About_sec1_data(request.POST,request.FILES,instance=uas1)
        if as1.is_valid():
            as1.save()
            return redirect('/view_about_sec1')
        else:
            print(as1.errors)
            return render(request,"About-Page/add-about_sec1.html",{"as1":as1})
    else:
        as1 = About_sec1_data(instance = uas1,initial={'as1image1': uas1.as1image1,'as2image2': uas1.as1image2, 'as1title': uas1.as1title, 'as1desc': uas1.as1desc})
    return render(request,"About-Page/add-about_sec1.html",{"as1":as1})

# =============================================== About sec 2 ==================================================================

def add_about_sec2(request):
    if 'admin_username' in request.session:
        as2 = About_sec2_data()

        if request.method == "POST":
            as2 = About_sec2_data(request.POST,request.FILES)
            as2.save()
            return redirect("/view_about_sec2")
    else:
        return redirect('/adminlogin')
    return render(request,"About-Page/add-about_sec2.html",{"as2":as2})


def view_about_sec2(request):
    if 'admin_username' in request.session:   
        about_sec2 = Aboutsec2.objects.all()    
    else:
        return redirect('/adminlogin')   
    return render(request,"About-Page/view-about_sec2.html",{"about_sec2":about_sec2})

def delete_about_sec2(request,id):
    if 'admin_username' in request.session:        
        delas2 = Aboutsec2.objects.get(id=id).delete()
        return redirect("/view_about_sec2")
    else:
        return redirect('/adminlogin')

def update_about_sec2(request,id):
    uas2 = get_object_or_404(Aboutsec2,id=id)
    if request.method == "POST":
        as2 = About_sec2_data(request.POST,request.FILES,instance=uas2)
        if as2.is_valid():
            as2.save()
            return redirect('/view_about_sec2')
        else:
            print(as2.errors)
            return render(request,"About-Page/add-about_sec2.html",{"as2":as2})
    else:
        as2 = About_sec2_data(instance = uas2,initial={'as2image1': uas2.as2image1, 'as2image2': uas2.as2image2,'as2title': uas2.as2title, 'as2desc': uas2.as2desc})
    return render(request,"About-Page/add-about_sec2.html",{"as2":as2})


# =============================================== Cart Page ==================================================================

def add_cart_header_img(request):
    if 'admin_username' in request.session:
        cart_himg = cart_header_data()

        if request.method == "POST":
            cart_himg = cart_header_data(request.POST,request.FILES)
            cart_himg.save()
            return redirect("/view_cart_header_img")
    else:
        return redirect('/adminlogin')
    return render(request,"Cart-Page/add-cart_header_image.html",{"cart_himg":cart_himg})


def view_cart_header_img(request):
    if 'admin_username' in request.session:   
        cart_header_img = cartheader.objects.all()    
    else:
        return redirect('/adminlogin')   
    return render(request,"Cart-Page/view-cart_header_image.html",{"cart_header_img":cart_header_img})

def delete_cart_header_img(request,id):
    if 'admin_username' in request.session:        
        delcart_headerimg = cartheader.objects.get(id=id).delete()
        return redirect("/view_cart_header_img")

def update_cart_header_img(request,id):
    ucart_himg = get_object_or_404(cartheader,id=id)
    if request.method == "POST":
        cart_himg = cart_header_data(request.POST,request.FILES,instance=ucart_himg)
        if cart_himg.is_valid():
            cart_himg.save()
            return redirect('/view_cart_header_img')
        else:
            print(cart_himg.errors)
            return render(request,"Cart-Page/add-cart_header_image.html",{"cart_himg":cart_himg})
    else:
        cart_himg = cart_header_data(instance = ucart_himg,initial={'cart_header_img': ucart_himg.cart_header_img,"cart_header_imgname":ucart_himg.cart_header_imgname})
    return render(request,"Cart-Page/add-cart_header_image.html",{"cart_himg":cart_himg})




# =============================================== Contact Page ==================================================================

def add_contact_header_img(request):
    if 'admin_username' in request.session:
        ch = contact_header_data()

        if request.method == "POST":
            ch = contact_header_data(request.POST,request.FILES)
            ch.save()
            return redirect("/view_contact_header_img")
    else:
        return redirect('/adminlogin')
    return render(request,"Contact-Page/add-header_image.html",{"ch":ch})


def view_contact_header_img(request):
    if 'admin_username' in request.session:   
        contact_header = contactheader.objects.all()    
    else:
        return redirect('/adminlogin')    
    return render(request,"Contact-Page/view-header_image.html",{"contact_header":contact_header})

def delete_contact_header_img(request,id):
    if 'admin_username' in request.session:        
        delcontact_headerimg = contactheader.objects.get(id=id).delete()
        return redirect("/view_contact_header_img")
    else:
        return redirect('/adminlogin')
    

def update_contact_header_img(request,id):
    uch = get_object_or_404(contactheader,id=id)
    if request.method == "POST":
        ch = contact_header_data(request.POST,request.FILES,instance=uch)
        if ch.is_valid():
            ch.save()
            return redirect('/view_contact_header_img')
        else:
            print(ch.errors)
            return render(request,"Contact-Page/add-header_image.html",{"ch":ch})
    else:
        ch = contact_header_data(instance = uch,initial={'contact_header_text': uch.contact_header_text,"contact_header_img":uch.contact_header_img})
    return render(request,"Contact-Page/add-header_image.html",{"ch":ch})



def add_contact_middele_img(request):
    if 'admin_username' in request.session:
        cm = contact_middle_data()

        if request.method == "POST":
            cm = contact_middle_data(request.POST,request.FILES)
            cm.save()
            return redirect("/view_contact_middele_img")
    else:
        return redirect('/adminlogin')
    return render(request,"Contact-Page/add-middele_image.html",{"cm":cm})


def view_contact_middele_img(request):
    if 'admin_username' in request.session:   
        contact_middele_img = contactmiddle.objects.all()    
    else:
        return redirect('/adminlogin')    
    return render(request,"Contact-Page/view-middele_image.html",{"contact_middele_img":contact_middele_img})

def delete_contact_middele_img(request,id):
    if 'admin_username' in request.session:        
        delcontact_middeleimg = contactmiddle.objects.get(id=id).delete()
        return redirect("/view_contact_middele_img")
    else:
        return redirect('/adminlogin')

def update_contact_middele_img(request,id):
    ucm = get_object_or_404(contactmiddle,id=id)
    if request.method == "POST":
        cm = contact_middle_data(request.POST,request.FILES,instance=ucm)
        if cm.is_valid():
            cm.save()
            return redirect('/view_contact_middele_img')
        else:
            print(cm.errors)
            return render(request,"Contact-Page/add-middele_image.html",{"cm":cm})
    else:
        cm = contact_middle_data(instance = ucm,initial={'contact_middle_img': ucm.contact_middle_img})
    return render(request,"Contact-Page/add-middele_image.html",{"cm":cm})



def add_contact_address(request):
    if 'admin_username' in request.session:   
        add_contact_address = contact_address_data()
        if request.method == "POST":
            add_contact_address = contact_address_data(request.POST,request.FILES)
            add_contact_address.save()
            return redirect('/view_contact_address_info')
        else:
            print(add_contact_address.errors)
    else:
        return redirect('/adminlogin')
    return render(request,"Contact-Page/add-contact_address.html",{"contact_address":add_contact_address})


def view_contact_address(request):
    if 'admin_username' in request.session:   
        viewcontact_address = contact_address.objects.all()
    else:
        return redirect('/adminlogin')
    return render(request,"Contact-Page/view-contact_address.html",{"viewcontact_address":viewcontact_address})

def delete_contact_address(request,id):
    if 'admin_username' in request.session:         
        delcontact_address = contact_address.objects.get(id=id).delete()
        return redirect('/view_contact_address_info')
    else:
        return redirect('/adminlogin')
    return redirect("/view_contact_address_info")


def update_contact_address(request,id):
    update_address = get_object_or_404(contact_address,id=id)
    if request.method == "POST":
        add_contact_address = contact_address_data(request.POST,request.FILES,instance=update_address)
        if add_contact_address.is_valid():
            add_contact_address.save()
            return redirect('/view_contact_address_info')
        else:
            print(add_contact_address.errors)
            return render(request,"Contact-Page/add-contact_address.html",{"contact_address":add_contact_address})
    else:
        add_contact_address = contact_address_data(instance = update_address,initial={ 'address': update_address.address, 'mobile': update_address.mobile,'email': update_address.email })
                                                          
    return render(request,"Contact-Page/add-contact_address.html",{"contact_address":add_contact_address})


def view_contact_messages(request):
    if 'admin_username' in request.session:   
        viewcontact_message = contact_message.objects.all()
    else:
        return redirect('/adminlogin')
    return render(request,"Contact-Page/view-contact_messages.html",{"viewcontact_message":viewcontact_message})

def delete_contact_messages(request,id):
    if 'admin_username' in request.session:         
        delcontact_message = contact_message.objects.get(id=id).delete()
        return redirect('/view_contact_address_info')
    else:
        return redirect('/adminlogin')
    return redirect("/view_contact_message")


# =============================================== Better Hygiene Section ==================================================================

def add_hsimage(request):
    if 'admin_username' in request.session:   
        if request.method == 'POST':
            hsbg = bh_background_data(request.POST, request.FILES)
            if hsbg.is_valid():
                hsbg.save()
                return redirect('/view_hygiene_sec_bg_img')
            else:
                print("Form errors:", hsbg.errors)
        else:
            hsbg = bh_background_data()
    else:
        return redirect('/adminlogin')
    return render(request, 'add-hygiene_sec_bg_img.html', {'hsbg': hsbg})

def view_hsimage(request):
    if 'admin_username' in request.session:   
        background_img = bh_background.objects.all()    
        # else:
        #     return redirect("/login/")    
    else:
        return redirect('/adminlogin')
    return render(request,"view-hygiene_sec_bg_img.html",{"background_img":background_img})

def delete_hsimage(request,id):
    if 'admin_username' in request.session:        
        delhs_background = bh_background.objects.get(id=id).delete()
        return redirect("/view_hygiene_sec_bg_img")
    else:
        return redirect('/adminlogin')

def update_hsimage(request,id):
    uhsbg = get_object_or_404(bh_background,id=id)
    if request.method == "POST":
        hsbg = bh_background_data(request.POST,request.FILES,instance=uhsbg)
        if hsbg.is_valid():
            hsbg.save()
            return redirect('/view_hygiene_sec_bg_img')
        else:
            print(hsbg.errors)
            return render(request,"add-hygiene_sec_bg_img.html",{"hsbg":hsbg})
    else:
        hsbg = bh_background_data(instance = uhsbg,initial={'image': uhsbg.image})
    return render(request,"add-hygiene_sec_bg_img.html",{"hsbg":hsbg})

# =============================================== Footer ==================================================================
def addfooter(request):
    if 'admin_username' in request.session:
        if request.method == 'POST':
            fd = FooterData(request.POST, request.FILES)
            if fd.is_valid():
                fd.save()
                return redirect('/viewfooter')
            else:
                print("Form errors:", fd.errors)
        else:
            fd = FooterData()
    else:
        return redirect('/adminlogin')
    return render(request, 'add-footer.html', {'fd': fd})

def viewfooter(request):
    if 'admin_username' in request.session:   
        footer = Footerimg.objects.all()    
    else:
        return redirect('/adminlogin')
    return render(request,"view-footer.html",{"footer":footer})

def deletefooter(request,id):
    if 'admin_username' in request.session:        
        delfooter = Footerimg.objects.get(id=id).delete()
        return redirect("/viewfooter")
    else:
        return redirect('/adminlogin')

def updatefooter(request,id):
    ufd = get_object_or_404(Footerimg,id=id)
    if request.method == "POST":
        fd = FooterData(request.POST,request.FILES,instance=ufd)
        if fd.is_valid():
            fd.save()
            return redirect('/viewfooter')
        else:
            print(fd.errors)
            return render(request,"add-footer.html",{"fd":fd})
    else:
        fd = FooterData(instance = ufd,initial={'fimage': ufd.fimage})
    return render(request,"add-footer.html",{"fd":fd})

# ================================================= Product ======================================================================
def add_category(request):
    if 'admin_username' in request.session:
        if request.method == "POST":
            categoryname = request.POST['categoryname']
            
            cat = Category(
                categoryname = categoryname,
                
            )
            cat.save()
            return redirect('/view_category')
    else:
        return redirect('/adminlogin')
    return render(request,"Product/add-category.html",{"cat":cat})

def view_category(request):
    if 'admin_username' in request.session:
        viewcategory = Category.objects.all()
    else:
        return redirect('/adminlogin')
    return render(request,"Product/view-category.html",{"viewcategory":viewcategory})
    
def delete_category(request,id):
    if 'admin_username' in request.session:        
        delcategory = Category.objects.get(id=id).delete()
        return redirect('/view_category')
    else:
        return redirect('/adminlogin')
        # else:
        #     return redirect('/login_admin/')
        return render(request,"add-mainmenu.html")


def update_category(request,id):
    if 'admin_username' in request.session:
        cat = Category.objects.filter(id=id).get()
        if request.method == "POST":
            categoryname = request.POST['categoryname']
            
            cat.categoryname=categoryname
            cat.save()
            return redirect('/view_category')
    
    else:
        return redirect('/adminlogin')

    return render(request,"Product/add-category.html",{'cat':cat})


def addproduct(request):
    if 'admin_username' in request.session:
        if request.method == 'POST':
            form = product_data(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
            # Handle checkbox values for product weights
                product.pweight_500gm = request.POST.get('pweight_500gm', False)
                product.pweight_1kg = request.POST.get('pweight_1kg', False)
                product.pweight_1_5kg = request.POST.get('pweight_1_5kg', False)
                product.pweight_2kg = request.POST.get('pweight_2kg', False)
                product.pweight_2_5kg = request.POST.get('pweight_2_5kg', False)
                product.pweight_3kg = request.POST.get('pweight_3kg', False)
                product.pweight_3_5kg = request.POST.get('pweight_3_5kg', False)
                product.pweight_4kg = request.POST.get('pweight_4kg', False)
                product.pweight_4_5kg = request.POST.get('pweight_4_5kg', False)
                product.pweight_5kg = request.POST.get('pweight_5kg', False)
                
                product.save()
                return redirect('view_product')
        
        else:
            form = product_data()
            
        cts = Category.objects.all()
    else:
        return redirect('/adminlogin')
    return render(request, 'Product/add-product.html', {'form': form,"cts": cts})


def viewproduct(request):
    if 'admin_username' in request.session:
        if "search" in  request.GET:
            search=request.GET["search"]
            viewpd = Product.objects.filter(pname__icontains=search).all()
        else:    
            viewpd = Product.objects.all()
            # viewct = subcats.objects.all()
            # viewsct = subcats.objects.all()
            paginator = Paginator(viewpd, 6)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
        # else:
        #     return redirect('/login_admin/')
        
        viewpd = Product.objects.all()
        weights = []
        for product in viewpd:
            if product.pweight_500gm:
                weights.append('500gm')
            if product.pweight_1kg:
                weights.append('1kg')
            if product.pweight_1_5kg:
                weights.append('1.5kg')
            if product.pweight_2kg:
                weights.append('2kg')
            if product.pweight_2_5kg:
                weights.append('2.5kg')
            if product.pweight_3kg:
                weights.append('3kg')
            if product.pweight_3_5kg:
                weights.append('3.5kg')
            if product.pweight_4kg:
                weights.append('4kg')
            if product.pweight_4_5kg:
                weights.append('4.5kg') 
            if product.pweight_5kg:
                weights.append('5kg')
            
    else:
        return redirect('/adminlogin')
    return render(request,"Product/view-product.html",{"viewpd":viewpd,"page_obj":page_obj,'weights': weights})

def deleteproduct(request,id):
    if 'admin_username' in request.session:        
        delpd = Product.objects.get(id=id)
        if delpd !=[]:
            delpd.delete()
            return redirect("/view_product")
    else:
        return redirect('/adminlogin')
    return render(request,"Product/add-product.html")

def updateproduct(request, uid):
    product = get_object_or_404(Product, id=uid)
    
    if request.method == "POST":
        form = product_data(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/view_product")
        else:
            print(form.errors)
            return render(request, "Product/add-product.html", {"form": form, "product": product})
    else:
        form = product_data(instance=product)
    
    cts = Category.objects.all()
    return render(request, "Product/add-product.html", {"form": form, "product": product, "cts": cts})



# ========================================================  Order page ==================================================================


def view_orders(request):
    if 'admin_username' in request.session:
        users = UserProfile.objects.all()
        orders = orders_item.objects.all()
        overall_total = sum(item.price for item in orders)
        return render(request,"view-order.html",{'users': users,
            'orders': orders,
            'overall_total': overall_total,})
    else:   
        return redirect('/adminlogin')

def view_orders_fulldetails(request,user_id,order_id):
    if 'admin_username' in request.session:
        user_profile = get_object_or_404(UserProfile, id=user_id)
        order = get_object_or_404(orders_item, id=order_id, user=user_profile)
        # orders = orders_item.objects.filter(user=user_profile)
        # overall_total = sum(item.price for item in order)
        return render(request,"order_fulldetails.html",{'user_profile': user_profile,
            'order': order,
            })
    else:
        return redirect('/adminlogin')
    
def delete_orders(request,order_id):
    if 'admin_username' in request.session:
        del_orders = orders_item.objects.filter(id=order_id).delete()
        return redirect('/view_orders')
        return render(request,"view-order.html")
    else:   
        return redirect('/adminlogin')


# ======================================================== User contact page ==================================================================

def add_contact_message(request):
    cm = contact_message_data()
    if request.method == "POST":
        cm = contact_message_data(request.POST,request.FILES)
        if cm.is_valid():
            cm.save()
            return redirect('/contact')
        else:
            print(cm.errors)
            return render(request,"contact_page.html",{"cm":cm})
    return render(request,"contact_page.html",{"cm":cm})

def view_contact_message(request):
    viewcm = contact_message.objects.all()
    return render(request,"contact_page.html",{"viewcm":viewcm})



# ======================================================== User contact page end ==================================================================


