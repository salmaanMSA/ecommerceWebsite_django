from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('overview/', overView, name="overView"),
    path('product/<int:id>/', productView, name="productView"),
    path('cart/', cartView, name='cart' ),
    path('', LoginView.as_view(), name="loginView"),
    path('deletecart/<int:id>/', deleteCartItem, name='deleteCart'),
    # path('updatecart/', updateCartItem, name="updateCart"),
    path('checkout/', checkOut, name="checkout"),

    path('register/', RegistrationView.as_view(), name="register"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-first_name', csrf_exempt(First_NameValidationView.as_view()), name="validate-first_name"),
    path('validate-last_name', csrf_exempt(Last_NameValidationView.as_view()), name="validate-last_name"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('validate-mobile_no', csrf_exempt(Mobile_NumberValidationView.as_view()), name="validate-mobile_no"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),
    path('logout/', LogoutView.as_view(), name="logout"),
]