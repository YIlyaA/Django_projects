from tkinter import CASCADE
from django.db import models
from django.urls import reverse

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    # class Meta:
        # db_table = 'category'

    def __str__(self):
        return self.name


class Products(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='goods_image', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE) 


    class Meta:
        ordering = ("id",)


    def __str__(self):
        return f'{self.name} Quantity - {self.quantity}'
    

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    


    def display_id(self):
        return f'{self.id:05}'


    def display_price_with_discount(self):
        return round(self.price - self.price*self.discount/100, 2)