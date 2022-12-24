from django.shortcuts import render
from .models import *

def brand(request):
    all_brand = Brands.objects.all()
    context= {'brand':all_brand}
    return render(request,'products\templates\pages\product.html',context)
