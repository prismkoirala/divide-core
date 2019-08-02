from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django import forms

STATES =[
    ('1','STATE 1'),
    ('2','STATE 2'),
    ('3','STATE 3'),
    ('4','STATE 4'),
    ('5','STATE 5')
]
# Create your models here.

CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sportswear'),
    ('OW','Outwear'),
)

LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)

LABEL_NAME_CHOICES = (
    ('New','New'),
    ('Prime','Prime'),
    ('Out Of Stock','Out Of Stock'),
)

ITEM_SIZE = (
    ('S','Small'),
    ('M','Medium'),
    ('L','Large'),
    ('XL','Extra Large')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True,null=True)
    image = models.ImageField(upload_to = 'product-img/',
        default='default/default-dummy-image.jpg',
        blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    label_name = models.CharField(choices=LABEL_NAME_CHOICES,max_length=12)
    slug = models.SlugField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    add_info = models.TextField()
    add_image1 = models.ImageField(upload_to = 'additional/',
        default='default/add_default.jpg',
        blank=True, null=True)
    add_image2 = models.ImageField(upload_to = 'additional/',
        default='default/add_default.jpg',
        blank=True, null=True)
    add_image3 = models.ImageField(upload_to = 'additional/',
        default='default/add_default.jpg',
        blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs = {
            'slug' : self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug' : self.slug
        })

    def get_add_to_cart_for_product_url(self):
        return reverse("core:add-to-cart-product", kwargs={
            'slug' : self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug' : self.slug
        })

    def percentage_off(self):
        if self.discount_price:
            discount = self.price - self.discount_price
            dis = (discount/self.price)*100
            return round(dis)
        else:
            pass


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(blank=True,choices = ITEM_SIZE, max_length=2, default="S",)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def total_before_discount(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddresse', on_delete=models.SET_NULL,
                    blank=True,
                    null = True
                    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_all_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_before_discount()
        return total

    def total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_before_discount() - order_item.get_final_price()
        return total

class BillingAddresse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    state = models.CharField(choices= STATES, max_length = 2)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
