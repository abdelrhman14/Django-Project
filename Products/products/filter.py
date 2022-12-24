from random import choice, choices
from unittest import result
from django import forms
import django_filters
from matplotlib import widgets
from brands.models import Brands

from .models import *

class CategoryFilter(django_filters.FilterSet):

    class Meta:
        model = Category
        fields = '__all__'
        exclude =['CATdescription','slug','image','CATname']

class ProductFilter(django_filters.FilterSet):


    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brands.objects.all(),
    widget=forms.CheckboxSelectMultiple)


    PRprice__gt = django_filters.NumberFilter(field_name='PRprice', lookup_expr='gt')
    PRprice__lt = django_filters.NumberFilter(field_name='PRprice', lookup_expr='lt')


    Choice = (('All Product','All Product'),
                ('New Product','New Product'),
                ('Bestseller Product','Bestseller Product'),
                ('Price low to high','Price low to high'),
                ('Price high to low','Price high to low'),
                ('High rated','High rated')
                )

    order = django_filters.ChoiceFilter(label='Sort by:', choices = Choice  , method='filter_order', empty_label=None,widget=forms.Select)

    def filter_order(self, queryset, name, value):
        if value == 'All Product':
            result = queryset.all()

        elif value == 'New Product':
            result = queryset.filter(PRnew=True)

        elif value == 'Bestseller Product':
            result = queryset.filter(PRbestseller=True)

        elif value == 'Price low to high':
            result = queryset.order_by('PRprice')

        elif value == 'Price high to low':
            result = queryset.order_by('-PRprice')

        return result



    class Meta:
        model = Products
        fields = '__all__'
        exclude =['category','pr_code','PRdescription','PRdiscount_price','PRstate','PRimage','PRnp_available','slug','created_at','updated_at']

class BrandFilter(django_filters.FilterSet):

    Bname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Brands
        fields = '__all__'
        exclude =['Bdescription']
