
from .models import Product, Registration, CustomUser, AddToCart
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from validate_email import validate_email
from django.contrib import messages, auth
from django.urls import reverse
from .utils import token_generator
# Create your views here.


def overView(request):
    """
        Product Overview
    """

    products = Product.objects.all()

    context = {
        'product':products,
    }

    return render(request, 'overview.html', context)

def productView(request,id):
    """
        Product Detail View
    """
    if request.method == 'GET':
        prod = Product.objects.filter(id=id)
        print(prod[0].product_id)
        context = {
            'product':prod[0]
        }
        return render(request, 'product.html', context)

    if request.method == 'POST':
        id = request.POST['id']
        product = Product.objects.get(id=id)
        quantity = int(request.POST['quantity'])
        amount = quantity*product.product_price
        add_to_cart =  AddToCart.objects.create(user=request.user, product_name=product.product_name, product_price=product.product_price,product_desc=product.product_desc, product_img=product.product_image,quantity=quantity,total_amount=amount)
        messages.success(request, "Product Added to Cart")
        return redirect('overView')


def cartView(request):

    if request.method == 'GET':
        cartItems = AddToCart.objects.all()

        Total_Amount = 0

        for i in cartItems:
            Total_Amount += i.total_amount
        Amount= Total_Amount

        context = {
            'items' : cartItems,
            'amount':Amount
        }
        return render(request, 'cart.html', context)

def deleteCartItem(request,id):
    if request.method == 'GET':
        item = AddToCart.objects.get(id=id)
        item.delete()
        messages.success(request, "Item removed from the Cart")
        return redirect('cart')

def updateCartItem(request):
    if request.method == 'POST':
        quantity = request.POST['quantity']
        print(quantity)
        return redirect('cart')

def checkOut(request):
    item = AddToCart.objects.filter(user=request.user)
    nitem = len(item)

    amt = 0
    for i in item:
        amt += i.total_amount
    total = amt
    # print(total)


    context = {
        'items':item,
        'nitem':nitem,
        'total_amt':total
    }
    return render(request, 'checkout.html', context)


class UsernameValidationView(View):
    """
        Username Validation for Register User
    """
    def post(self, request):

        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric character!!!'},
                                status=400)

        if Registration.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, username in use choose another one!!!'}, status=409)

        return JsonResponse({'username_valid': True})


class First_NameValidationView(View):
    """
        First Name Validation for Register User
    """
    def post(self, request):

        data = json.loads(request.body)
        first_name = data['first_name']

        if not str(first_name).isalpha():
            return JsonResponse({'first_name_error': 'First Name should only contain alphabets!!!'},
                                status=400)

        return JsonResponse({'first_name_valid': True})


class Last_NameValidationView(View):
    """
        Last Name Validation for Register User
    """
    def post(self, request):

        data = json.loads(request.body)
        last_name = data['last_name']

        if not str(last_name).isalpha():
            return JsonResponse({'last_name_error': 'Last Name should only contain alphabets!!!'},
                                status=400)

        return JsonResponse({'last_name_valid': True})


class EmailValidationView(View):
    """
        Email Validation for Register User
    """
    def post(self, request):

        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email id is Invalid!!!!!'}, status=400)

        if Registration.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email in use choose another one!!!'}, status=409)

        return JsonResponse({'email_valid': True})


class Mobile_NumberValidationView(View):
    """
        Mobile Number Validation for Register User
    """
    def post(self, request):

        data = json.loads(request.body)
        mobile_no = data['mobile_no']

        if not mobile_no.isnumeric():
            return JsonResponse({'mobile_no_error': 'Mobile Number should only contain numeric character!!!'},
                                status=400)

        if Registration.objects.filter(mobile_no=mobile_no).exists():
            return JsonResponse({'mobile_no_error': 'Sorry, Mobile Number is already in use choose another!!!'},
                                status=409)

        return JsonResponse({'Mobile_no': True})


class RegistrationView(View):
    """
        Registeration View For Register New User
    """
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # Create a user account
        data = request.POST
        print(data)
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        mobile_no = request.POST['mobile_no']

        context = {
            'fieldValues': request.POST
        }

        if not Registration.objects.filter(email=email).exists():

            if not Registration.objects.filter(mobile_no=mobile_no).exists():

                if len(password) < 6:

                    messages.error(request, "Password too short")
                    return render(request, 'register.html', context=context)
                """
                    Saving User Registeration  details in Database
                """
                user = Registration.objects.create(first_name=first_name, last_name=last_name,
                                                   email=email, mobile_no=mobile_no, password=password)

                """
                    Creating Custom_user for Login Credentials
                """
                custom_user = CustomUser.objects.create_user(user_id=user, email=email, password=password)

                """
                    Generating token for link 
                """
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                """
                    Sending Email to the Registered User for Account Validation 
                """
                activate_url = 'http://' + domain + link
                email_subject = "Activate Your Account"
                email_body = 'Hello' + '' + user.first_name + '' \
                                                              '\nPlease use this link to verify your Account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account Created Successfully")
                messages.info(request, 'Please Check Your Registered email id for Account Validation')
                return render(request, 'register.html')

        return render(request, 'register.html')


class VerificationView(View):
    """
        Verification of Email Validation
    """
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = Registration.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('loginView' + '?message=' + 'User Already Activated')
            """
                If User is Active then Redirecting the User to Login Page
            """
            if user.is_active:
                return redirect('loginView')

            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated Successfully')
            return redirect('loginView')

        except Exception as e:
            pass

        return redirect('loginView')


class LoginView(View):
    """
        Landing Page with Login Functionality
    """
    def get(self, request):
        return render(request, 'landing_page.html')

    def post(self, request):

        email = request.POST['email']
        password = request.POST['password']

        """
            Login Authentication
        """
        if email and password:
            user = auth.authenticate(email=email, password=password)

            if user:

                if user.is_active:
                    """
                        If User is Active then Redirecting to Dashboard
                    """
                    auth.login(request, user)
                    user = Registration.objects.get(email=email)
                    messages.success(request, 'Welcome' + "..." + user.first_name + "," + "You are now logged in...")
                    return redirect('overView')

                else:
                    messages.error(request, 'Account not active, Please check your registered mail..!!!')
                    return render(request, 'landing_page.html')
            else:
                messages.error(request, 'Invalid Credentials, Please try again..!!!')
                return render(request, 'landing_page.html')
        else:
            messages.error(request, 'Please Fill all fields..!!!')
            return render(request, 'landing_page.html')


class LogoutView(View):
    """
        Logout Functionality
    """
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been Logged out')
        return redirect('loginView' )
