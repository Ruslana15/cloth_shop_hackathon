from django.db import models
from django.contrib.auth import get_user_model
from django.forms import CharField, ChoiceField
from slugify import slugify
from .utils import get_time
from django.db.models import Sum



User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    parent_category = models.ForeignKey(
        verbose_name='Родительская категория',
        to='self', 
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True
         )
    
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Category'


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, primary_key=True, blank=True)
    description = models.TextField()
    consists_of = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name='Состоит из'
        )
    color1 = models.CharField(max_length=20 , null=True)
    color2 = models.CharField(max_length=20, blank=True, null=True)
    CHOICES = (
        ('s', 'S / 46-48'),
        ('m', 'M / 48-50'),
        ('l', 'L / 50-52'),
        ('xl', 'XL / 52-54'),
        ('xxl', 'XXl / 54-56'),
    )
    size1 = models.CharField(max_length=10, choices=CHOICES, null=True)
    size2 = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    size3 = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    size4 = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    size5 = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Скидка'
        )
    quantity = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    image = models.ImageField(upload_to='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='products')
    # user = models.ForeignKey(
    #     to=User,
    #     on_delete=models.CASCADE,
    #     related_name='products'
    # )

    
    
    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/carousel')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_images'
    )

    def __str__(self) -> str:
        return f"Image to {self.product.title}"



