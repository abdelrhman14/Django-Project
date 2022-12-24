from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from matplotlib.style import context
from requests import request
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required

from products.forms import CommentForm,Crowd_Form,Edit_Crowd_Form
from .models import *
from .filter import *
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect




def home(request):

    context_dict={}

    category_list = Category.objects.filter(CATparent=None).order_by('id')
    context_dict['category_list'] = category_list

    all_product = Products.objects.all().order_by('id')[0:4]
    context_dict['all_product'] = all_product

    new_product = Products.objects.filter(PRnew=True)[0:4]
    context_dict['new_product'] = new_product

    bestseller_product = Products.objects.filter(PRbestseller=True)[0:4]
    context_dict['bestseller_product'] = bestseller_product

    sale_product = Products.objects.filter(PRdiscount_price__gt=0)[0:4]
    context_dict['sale_product'] = sale_product

    last_product = Products.objects.all().order_by('-id')[0:4]
    context_dict['last_product'] = last_product
    
    return render(request,'pages/index.html',context_dict)


def product(request,slug):

    context_dict={}
    
    try:
        category = Category.objects.get(slug=slug)
        context_dict['category'] = category
        context_dict['category_name'] = category.CATname

        product_list = Products.objects.filter(category=category)
        myfilter = ProductFilter(request.GET,queryset=product_list)
        product_list = myfilter.qs

        context_dict['product_list'] = product_list
        context_dict['myfilter'] = myfilter

        product_count = product_list.count()
        context_dict['product_count'] = product_count

        category_child = Category.objects.filter(CATparent=category).order_by('id')

        if request.method == 'GET':
            search_category = request.GET.get('search-category')
            if search_category!= '' and search_category is not None:
                category_child = category_child.filter(CATname__icontains=search_category)

        context_dict['category_child'] = category_child

    except Category.DoesNotExist:
        pass

    return render(request,'pages/product.html',context_dict)

def product_details(request,slug):

    context_dict = {}

    products_details = get_object_or_404(Products,slug=slug)
    context_dict['products_details'] = products_details
    
    related_products = Products.objects.filter(brand=products_details.brand)[0:3]
    context_dict['related_products'] = related_products

    try:
        order = OrderItem.objects.get(user=request.user,product=products_details)
        context_dict['order'] = order
    except:
        pass

    try:
        product_alt = Product_Alternative.objects.get(PlaneA_product=products_details)
        context_dict['product_alt'] = product_alt

    except Product_Alternative.DoesNotExist:
        pass

    comments = products_details.comments.all()
    context_dict['comments'] = comments

    # Add Comment
    form =CommentForm(instance = products_details)
    if request.method =='POST':
        form =CommentForm(request.POST,instance = products_details)
        if form.is_valid():
            user = request.user
            comment = form.cleaned_data['comment']
            new_comment = Comment.objects.create(product = products_details, user=user, comment=comment)
            new_comment.save()
    else:
        form = CommentForm()
        
    context_dict['form'] = form


    # Update Comment
    if request.method =='POST':
        comment = form.cleaned_data['comment']
        form =CommentForm(instance = comment)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
        
    context_dict['form'] = form
    return render(request,'pages/product_details.html',context_dict)


def add_to_cart(request,slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Products,slug=slug)
        user = request.user
        order_item, created = OrderItem.objects.get_or_create(product=product,user=user)
        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(product__slug = product.slug).exists():
                order_item.qunatity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))                   
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

def remove_single_item_from_cart(request,slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Products,slug=slug)
        user = request.user
        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(product__slug = product.slug).exists():
                order_item= OrderItem.objects.filter(product=product,user=user)[0]
                if order_item.qunatity > 1:
                    order_item.qunatity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                    order_item.delete()
                messages.info(request, "This item quantity was updated.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(request, "This item was not in your cart")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.info(request, "You do not have an active order")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                 

def remove_from_cart(request, slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Products,slug=slug)
        user = request.user
        order_qs = Order.objects.filter(user=user)
        try:
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(product__slug = product.slug).exists():
                    order_item= OrderItem.objects.filter(product=product,user=user)[0]
                    order.items.remove(order_item)
                    order_item.delete()
                    messages.info(request, "This item was removed from your cart.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.info(request, "This item was not in your cart")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(request, "You do not have an active order")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            pass
        

def OrderSummary(request):
    if request.user.is_authenticated:

        context_dict = {}

        order = Order.objects.get(user=request.user)
        context_dict['order'] = order

        last_product = Products.objects.all().order_by('-id')[0:4]
        context_dict['last_product'] = last_product

        all_items = order.items.all()
        context_dict['all_items'] = all_items


    
        return render(request,'pages/order_summary.html', context_dict)

def add_comment(request,slug):
    if request.user.is_authenticated:
        

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        


        
def update_comment(request,slug):
    pass

def delete_comment(request,slug):
    pass



'''
        


def add_to_cart(request,slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Products,slug=slug)
        user = request.user
        order_item, created = OrderItem.objects.get_or_create(product=product,user=user)
        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(product__slug = product.slug).exists():
                order_item.qunatity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("/products",slug=slug)

            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("/products",slug=slug)
                   
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("/products",slug=slug)

def remove_single_item_from_cart(request,slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Products,slug=slug)
        user = request.user
        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(product__slug = product.slug).exists():
                order_item= OrderItem.objects.filter(product=product,user=user)[0]
                if order_item.qunatity > 1:
                    order_item.qunatity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                messages.info(request, "This item quantity was updated.")
                return redirect("/products",slug=slug)
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("core:product", slug=slug)

        else:
            messages.info(request, "You do not have an active order")
            return redirect("/products",slug=slug)
                 
        
def search(request):
    context_dict={}
    
    category_list = Category.objects.filter(CATparent=None).order_by('id')
    context_dict['category_list'] = category_list

    if request.method == 'GET':
        search_all = request.GET['search-all']
        if search_all!='' and search_all is not None:
            multiply_product = Q(Q(PRname__icontains = search_all))
            multiply_category = Q(Q(CATname__icontains = search_all))

            data_product = Products.objects.filter(multiply_product)
            data_category = Category.objects.filter(multiply_category)

    
    context_dict['data_product'] = data_product
    context_dict['data_category'] = data_category



    context_dict['search_name'] = search_all

    count = data_product.count()
    context_dict['count'] = count

    return render(request,'pages/search.html',context_dict)


        brand = Brands.objects.all()
        my_filter2 = BrandFilter(request.GET,queryset=brand)
        context_dict['my_filter2'] = my_filter2
        




                


        all_category = Category.objects.all()
        context_dict['all_category'] = all_category
        
        all_brand = Brands.objects.all()
        context_dict['all_brand'] = all_brand

def filter(request):
    product = Products.objects.all()
    myfilter = ProductFilter(request.GET,queryset=product)
    product = myfilter.qs
    context={'product':product,'myfilter':myfilter}
    return render(request,'pages/filter_pages.html',context)

product = Products.objects.all()
    price_q = request.GET.get('searched')
    if price_q != '' and price_q is not None:
        product = product.filter(PRprice=price_q)
    context={'qs':product}'''

    