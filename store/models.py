from django.db import models


# =========================
# PRODUCT
# =========================

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('dresses', 'Dresses'),
        ('tops', 'Tops'),
        ('accessories', 'Accessories'),
        ('jewellery', 'Jewellery'),
        ('shoes', 'Shoes'),
    ]

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField(
        default=0
    )

    size = models.CharField(
        max_length=20,
        blank=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='dresses'
    )


    def __str__(self):
        return self.name


# =========================
# ORDER
# =========================

class Order(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.customer_name


# =========================
# ORDER ITEM
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    size = models.CharField(
        max_length=20,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):
        return (
            f"{self.product.name} "
            f"x {self.quantity}"
        )


# =========================
# CONTACT MESSAGE
# =========================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name