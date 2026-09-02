"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store.views import (
    product_list,
    product_detail,
    add_to_cart,
    cart,
    remove_from_cart,
    increase_quantity,
    decrease_quantity,
    checkout,
    register,
    user_login,
    user_logout,
    my_orders,
    about,
    contact,
)


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),


    # =========================
    # PRODUCTS
    # =========================

    path(
        '',
        product_list,
        name='product_list'
    ),

    path(
        'shop/',
        product_list,
        name='shop'
    ),

    path(
        'product/<int:product_id>/',
        product_detail,
        name='product_detail'
    ),


    # =========================
    # CART
    # =========================

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart,
        name='cart'
    ),

    path(
        'remove-from-cart/<str:cart_key>/',
        remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase/<str:cart_key>/',
        increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<str:cart_key>/',
        decrease_quantity,
        name='decrease_quantity'
    ),


    # =========================
    # CHECKOUT
    # =========================

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),


    # =========================
    # ORDERS
    # =========================

    path(
        'my-orders/',
        my_orders,
        name='my_orders'
    ),


    # =========================
    # ABOUT & CONTACT
    # =========================

    path(
        'about/',
        about,
        name='about'
    ),

    path(
        'contact/',
        contact,
        name='contact'
    ),

]


# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )