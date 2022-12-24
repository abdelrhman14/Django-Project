from pyexpat import model
from turtle import title
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save

class Crowd_Funding(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    title = models.CharField(max_length=50,verbose_name=('Title'),null=True,blank=True)
    details = models.TextField(verbose_name='Details',null=True,blank=True)
    total_target = models.IntegerField(verbose_name='Total_Target',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')

    class Meta:
        verbose_name = 'Crowd Funding'
        verbose_name_plural = 'Crowd Funding'


class Category(models.Model):
    CATname = models.CharField(max_length=50,null=True,blank=True,verbose_name='Category Name')
    CATdescription = models.TextField(null=True,blank=True,verbose_name='Description')
    CATparent = models.ForeignKey('self',limit_choices_to={'CATparent__isnull':True},null=True,blank=True,verbose_name='Category Parent',on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,verbose_name='Image')
    slug = models.SlugField(null=True,blank=True,verbose_name='Slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.CATname)
        return super(Category,self).save(*args, **kwargs)

    
    def get_category_url(self):
       return reverse("category", kwargs={'slug': self.slug})


    def __str__(self):
        return str(self.CATname)

class Products(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE,verbose_name='Category')
    brand = models.ForeignKey('brands.Brands',on_delete=models.CASCADE,verbose_name='Brands',null=True,blank=True)
    PRname = models.CharField(max_length=250,null=True,blank=True,verbose_name='Product Name')
    PRdescription = models.TextField(verbose_name=('Description'),null=True,blank=True)
    PRinformation = models.TextField(verbose_name=('Information'),null=True,blank=True)
    pr_code = models.CharField(max_length=250,null=True,blank=True,verbose_name='Product Code')
    PRprice = models.FloatField(null=True,blank=True,verbose_name='Price')
    PRdiscount_price = models.FloatField(null=True,blank=True,verbose_name='Discount Price')
    PRstate = models.BooleanField(null=True,blank=True,verbose_name='is_active')
    PRimage = models.ImageField(verbose_name='Image',null=True,blank=True)
    PRnp_available = models.IntegerField(null=True,blank=True,verbose_name='Number Available')
    PRnew = models.BooleanField(default=True,verbose_name='New | Not')
    PRbestseller = models.BooleanField(default=False,verbose_name='Bestseller | Not')
    slug = models.SlugField(unique=True,blank=True, null=True,verbose_name='Slug')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='updated_at')
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.PRname)
        return super(Products,self).save(*args, **kwargs)

    def get_product_details_url(self):
       return reverse("product_details", kwargs={'slug': self.slug})
 
    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_single_item_url(self):
        return reverse("remove_single_item", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={
            'slug': self.slug
        })


    def discount_number(self):
        number = self.PRprice - self.PRdiscount_price
        return number
    def discount_percentage(self):
        total =  (1 - self.PRdiscount_price / self.PRprice) * 100
        return total
    
    def __str__(self):
        return self.PRname

class ProductsImage(models.Model):
    product = models.ForeignKey('Products',on_delete=models.CASCADE,null=True,blank=True)
    image = models.FileField(upload_to = 'images/',verbose_name='Image',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='updated_at')

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

class Product_Alternative(models.Model):
    PlaneA_product = models.ForeignKey(Products,related_name='main_product',on_delete=models.CASCADE)
    PlaneB_product = models.ManyToManyField(Products,related_name='alternative_product')


    class Meta:
        verbose_name = 'Product alternative'
        verbose_name_plural = 'Product alternatives'

    def __str__(self):
        return str(self.PlaneA_product)

class Product_Accessories(models.Model):
    PlaneA_product = models.ForeignKey(Products,related_name='main_Accessories',on_delete=models.CASCADE)
    PlaneB_PRODUCT = models.ManyToManyField(Products,related_name='accessories_product')

    class Meta:
        verbose_name = 'Product Accessory'
        verbose_name_plural = 'Product Accessories'

    def __str__(self):
        return str(self.PlaneA_product)

class OrderItem(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qunatity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')

    class Meta:
        verbose_name = 'OrderItems'
        verbose_name_plural = 'OrderItemss'

    def get_total_item_price(self):
        return self.qunatity * self.product.PRprice

    def get_total_discount_item_price(self):
        return self.qunatity * self.product.PRdiscount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.PRdiscount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def __str__(self):
        return f"{self.qunatity} of {self.product.PRname}"



    
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem,related_name='items')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_discount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_discount_item_price()
        return total

    def __str__(self):
        return self.user.username


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = CountryField()
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')

    class Meta:
        verbose_name = 'ShippingAddress'
        verbose_name_plural = 'ShippingAddress'

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created_at')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return str(self.user.username)





'''

from django.db.models.signals import pre_save
def validate_order(sender, instance, **kwargs):
    if instance.quantity < instance.inventory_item.quantity: # order can be fulfilled
        instance.save()
    else:
        # write logic to reject save and give message why

pre_save.connect(validate_order, sender=Order)

'''


'''

from django.db.models.signals import post_save
from myapp.utils import send_notification

def notify_user(sender, instance, **kwargs):
   send_notification(instance.ordered_by)

post_save.connect(notify_user, sender=Order)

With this, once an order is successfully placed, the client will be notified via email or text, depending on what the business use case demands.


Categories

Everyday Deals

Search for products or brands
Search
My Account

 Cart
Daily Deals
Daily Deals

Mobiles & Tablets

TVs

Personal Care

Small Home Appliances

Large Home Appliances

Laptops & PCs

Electronics
'''