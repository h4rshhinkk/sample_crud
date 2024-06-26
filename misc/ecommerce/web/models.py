from django.db import models

# Create your models here.


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
    keyword = models.CharField(max_length=200,blank=True,null=True)
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
        
    
class Variants(models.Model):
    variant_name = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/', blank=True,null=True)
    description = models.CharField(max_length=100, blank=True,null=True)
    quantity = models.IntegerField(default=1)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.variant_name