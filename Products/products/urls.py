from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    #path('',views.home,name='home'),
    path('category/<slug:slug>/',views.product,name='category'),
    path('product_details/<slug:slug>/',views.product_details,name='product_details'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single-item/<slug:slug>/',views.remove_single_item_from_cart,name='remove_single_item'),
    path('remove-from-cart/<slug:slug>',views.remove_from_cart,name='remove_from_cart'),
    path('OrderSummary/',views.OrderSummary,name='OrderSummary'),

]
