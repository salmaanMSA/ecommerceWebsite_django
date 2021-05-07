from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4

# Create your models here.
"""
    Creating Product Model
"""

class Product(models.Model):
    product_id = models.AutoField
    product_image = models.ImageField(upload_to="static/images", null=False)
    product_name = models.CharField(max_length=50, null=False)
    product_desc = models.CharField(max_length=300, null=True)
    product_price = models.IntegerField(null=False)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    pub_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name


"""
    Creating User Registeration Model
"""

class Registration(models.Model):

    user_id = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    first_name = models.CharField(max_length=55, null=False)
    last_name = models.CharField(max_length=55, null=True)
    email = models.EmailField(max_length=100, unique=True, null=False)
    mobile_no = models.IntegerField(unique=True, null=False)
    password = models.CharField(max_length=16, null=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


"""
    Custom User Model creation
"""

class UserManager(BaseUserManager):
    """
        Custom User Manager
    """

    def create_user(self, email=str, password=str, **extra_fields):
        """
            Create Normal User
        :return: string
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=str, password=str, **extra_fields):
        """
            Create Super user
        :param email:
        :param password:
        :param extra_fields:
        :return: string
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        Custom User table desc
    """
    id = models.UUIDField(default=uuid4, primary_key=True)
    user_id = models.ForeignKey(to=Registration, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=255, null=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

"""
    Add to Cart Model
"""

class AddToCart(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, null=False)
    product_price = models.IntegerField(null=False)
    product_desc = models.CharField(max_length=300)
    product_img = models.ImageField()
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name
