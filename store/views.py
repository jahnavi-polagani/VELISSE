from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .models import Product, Order, OrderItem, ContactMessage


# =========================
# PRODUCT LIST
# =========================

def product_list(request):

    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(
        request,
        'store/products.html',
        {
            'products': products
        }
    )


# =========================
# PRODUCT DETAIL
# =========================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )


# =========================
# ADD TO CART
# =========================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    cart = request.session.get(
        'cart',
        {}
    )


    product_id = str(product_id)


    # Get selected size from the form
    size = request.POST.get(
        'size',
        ''
    ).strip()


    # Dresses must have a size
    if product.category == 'dresses' and not size:

        return redirect(
            'product_detail',
            product_id=product.id
        )


    # Create a unique cart key.
    #
    # This allows the same dress to be
    # added in different sizes.
    #
    # Example:
    # 5_M
    # 5_L

    if product.category == 'dresses':

        cart_key = f"{product_id}_{size}"

    else:

        cart_key = product_id


    # If product already exists in cart,
    # increase its quantity.

    if cart_key in cart:

        item = cart[cart_key]


        if isinstance(item, dict):

            item['quantity'] = (
                item.get('quantity', 1) + 1
            )

            item['size'] = size


        else:

            cart[cart_key] = {
                'quantity': item + 1,
                'size': size
            }


    else:

        cart[cart_key] = {

            'quantity': 1,

            'size': size

        }


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')

def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    products = []

    total = 0


    for cart_key, item in cart_data.items():

        # New cart format
        if isinstance(item, dict):

            quantity = item.get(
                'quantity',
                1
            )

            size = item.get(
                'size',
                ''
            )

        # Old cart format
        else:

            quantity = item

            size = ''


        # --------------------------------
        # Get actual product ID
        # --------------------------------

        if '_' in str(cart_key):

            product_id = str(
                cart_key
            ).split('_')[0]

        else:

            product_id = str(
                cart_key
            )


        product = get_object_or_404(
            Product,
            id=product_id
        )


        subtotal = (
            product.price * quantity
        )

        total += subtotal


        products.append({

            'product': product,

            'quantity': quantity,

            'size': size,

            'subtotal': subtotal,

            'cart_key': cart_key

        })


    return render(
        request,
        'store/cart.html',
        {
            'products': products,

            'total': total
        }
    )


def remove_from_cart(
    request,
    cart_key
):

    cart = request.session.get(
        'cart',
        {}
    )


    if cart_key in cart:

        del cart[cart_key]


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')


def increase_quantity(
    request,
    cart_key
):

    cart = request.session.get(
        'cart',
        {}
    )


    if cart_key in cart:

        item = cart[cart_key]


        if isinstance(item, dict):

            item['quantity'] = (
                item.get(
                    'quantity',
                    1
                ) + 1
            )

        else:

            cart[cart_key] = item + 1


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')


def decrease_quantity(
    request,
    cart_key
):

    cart = request.session.get(
        'cart',
        {}
    )


    if cart_key in cart:

        item = cart[cart_key]


        if isinstance(item, dict):

            item['quantity'] = (
                item.get(
                    'quantity',
                    1
                ) - 1
            )


            if item['quantity'] <= 0:

                del cart[cart_key]


        else:

            cart[cart_key] = item - 1


            if cart[cart_key] <= 0:

                del cart[cart_key]


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')

# =========================
# CHECKOUT
# =========================

def checkout(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    products = []

    total = 0


    # =========================
    # GET CART PRODUCTS
    # =========================

    for cart_key, item in cart_data.items():

        # -------------------------
        # Get actual product ID
        # -------------------------

        if '_' in str(cart_key):

            product_id = str(
                cart_key
            ).split('_')[0]

        else:

            product_id = str(
                cart_key
            )


        product = get_object_or_404(
            Product,
            id=product_id
        )


        # -------------------------
        # Get quantity and size
        # -------------------------

        if isinstance(item, dict):

            quantity = item.get(
                'quantity',
                1
            )

            size = item.get(
                'size',
                ''
            )

        else:

            quantity = item

            size = ''


        # -------------------------
        # Calculate subtotal
        # -------------------------

        subtotal = (
            product.price * quantity
        )

        total += subtotal


        products.append({

            'product': product,

            'quantity': quantity,

            'size': size,

            'subtotal': subtotal

        })


    # =========================
    # EMPTY CART
    # =========================

    if not products:

        return redirect('cart')


    # =========================
    # PLACE ORDER
    # =========================

    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name'
        )

        email = request.POST.get(
            'email'
        )

        phone = request.POST.get(
            'phone'
        )

        address = request.POST.get(
            'address'
        )


        # =========================
        # CREATE ORDER
        # =========================

        order = Order.objects.create(

            user=(
                request.user
                if request.user.is_authenticated
                else None
            ),

            customer_name=customer_name,

            email=email,

            phone=phone,

            address=address,

            total_price=total

        )


        # =========================
        # CREATE ORDER ITEMS
        # =========================

        for item in products:

            OrderItem.objects.create(

                order=order,

                product=item['product'],

                quantity=item['quantity'],

                size=item['size'],

                price=item['product'].price

            )


        # =========================
        # CLEAR CART
        # =========================

        request.session['cart'] = {}

        request.session.modified = True


        # =========================
        # SUCCESS PAGE
        # =========================

        return render(

            request,

            'store/order_success.html',

            {
                'customer_name':
                    customer_name
            }

        )


    # =========================
    # CHECKOUT PAGE
    # =========================

    return render(

        request,

        'store/checkout.html',

        {
            'products': products,

            'total': total
        }

    )
# =========================
# REGISTER
# =========================

def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'store/register.html',
                {
                    'error':
                    'Username already exists.'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        return redirect(
            'product_list'
        )

    return render(
        request,
        'store/register.html'
    )




# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )


        user = authenticate(

            request,

            username=username,

            password=password

        )


        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'product_list'
            )


        return render(
            request,
            'store/login.html',
            {
                'error':
                'Invalid username or password.'
            }
        )


    return render(
        request,
        'store/login.html'
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect(
        'product_list'
    )


# =========================
# MY ORDERS
# =========================

def my_orders(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )


    return render(
        request,
        'store/my_orders.html',
        {
            'orders': orders
        }
    )


# =========================
# ABOUT
# =========================

def about(request):

    return render(
        request,
        'store/about.html'
    )


# =========================
# CONTACT
# =========================

def contact(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        email = request.POST.get(
            'email'
        )

        message = request.POST.get(
            'message'
        )


        ContactMessage.objects.create(

            name=name,

            email=email,

            message=message

        )


        return render(
            request,
            'store/contact.html',
            {
                'success':
                'Your message has been sent successfully.'
            }
        )


    return render(
        request,
        'store/contact.html'
    )