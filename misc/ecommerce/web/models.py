from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

USER_STATUS =(
    (1,'pending'),
    (2,'active'),
    (3,'blocked'),
    (4,'deleted'),
)

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile = models.CharField(max_length=225, blank=True)
    profile_pic = models.ImageField(upload_to='profile', blank=True, null=True)
    address = models.CharField(max_length=225, blank=True)
    email_stat = models.BooleanField(default=False)
    mobile_stat = models.BooleanField(default=False)
    status = models.PositiveIntegerField(choices=USER_STATUS,null=False,blank=False,default=1)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email + ' - ' + self.first_name + ' ' + self.last_name

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200,)
    description = models.TextField(blank=True)
    p_keyword = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
    def get_default_media(self):
        return self.productmedia_set.filter(is_default=True, is_active=True).first()
    
class ProductMedia(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/', blank=True,null=True)
    is_default = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name
        
    
class ProductVariant(models.Model):
    variant_name = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/', blank=True,null=True)
    description = models.CharField(max_length=100, blank=True,null=True)
    quantity = models.IntegerField(default=1)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.variant_name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_name(self):
        return self.product

    def get_total_price(self):
        return self.quantity * self.product.sale_price

    def cart_total(self):
        return float(sum(item.get_total_price() for item in Cart.objects.filter(user=self.user)))

    def __str__(self):
        return f"{self.user}'s cart - {self.product} - {self.quantity}"