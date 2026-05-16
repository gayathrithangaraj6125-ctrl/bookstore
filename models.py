from django.db import models
from django.contrib.auth.models import User


# CATEGORY MODEL

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# BOOK MODEL

class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='books/'
    )

    rating = models.FloatField(default=0)

    summary = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.title


# CART MODEL

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


# WISHLIST MODEL

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} Wishlist"


# ORDER MODEL

class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_price = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=100,
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id}"