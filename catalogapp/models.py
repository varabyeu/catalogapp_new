from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Class describes main characteristics of product category in catalogapp"""
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        """Function represents category in admin"""
        return self.name

    def get_abs_url(self):
        """Function get absolute url using slug of category"""
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """This class describes main product characteristics"""

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Name of product')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        """Function represents product in admin"""
        return self.name

    def get_model_name(self):
        """Function returns model name in lowercase"""
        return self.__class__.__name__.lower()

    def get_abs_url(self):
        """Get absolute URL"""
        return reverse('product_detail', kwargs={'slug': self.slug})


class SelectedProduct(models.Model):
    """This class describes selecting products to Selection"""
    user = models.ForeignKey('UserClass', verbose_name='User', on_delete=models.CASCADE, related_name='customer')
    selected_item = models.ForeignKey('Selection', verbose_name='Selected items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total cost')

    def __str__(self):
        """Function represents boiler in admin.

        It makes using category name and name of current product
        """
        return 'Product is {} (for Selection)'.format(self.product.name)

    def save(self, *args, **kwargs):

        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Selection(models.Model):
    """Class Selection

    This class used to represent selected base product(selection)
    and dependent it(they) products
    """
    owner = models.ForeignKey('UserClass', null=True, verbose_name='Owner', on_delete=models.CASCADE)
    products = models.ManyToManyField(SelectedProduct, blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Total cost')
    in_order = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        """Function returns id of selection in string formation"""
        return str(self.id)


class UserClass(models.Model):
    """UserClass describes main characteristics of user.

    Now this class cannot to add other user any other except admin (me)
    """
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First name', null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Last name', null=True, blank=True)
    position = models.CharField(max_length=255, verbose_name='Position', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='User\'selection order')

    def __str__(self):
        """Function represent class in admin using first_name, last_name, position"""
        return 'User: {} {}, {}'.format(self.first_name, self.last_name, self.position)


class Order(models.Model):
    """Order class

     Class collects all needed info to represent order using
     views.py and checkout.html
     """
    STATUS_NEW = 'new'
    STATUS_INPROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    ORDER_TYPE_SELF = 'self'
    ORDER_TYPE_FOR_CUSTOMERS = 'For customers'

    STATUS_CHOISES = (
        (STATUS_NEW, 'New order'),
        (STATUS_INPROGRESS, 'Currently in progress'),
        (STATUS_READY, 'Ready to send'),
        (STATUS_COMPLETED, 'Already sent')
    )

    ORDER_TYPE_CHOIСE = (
        (ORDER_TYPE_SELF, 'For own needs'),
        (ORDER_TYPE_FOR_CUSTOMERS, 'For customers')
    )

    user = models.ForeignKey(UserClass, verbose_name='User', on_delete=models.CASCADE)
    selection = models.ForeignKey(
        Selection,
        verbose_name='Selection',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    to_project = models.CharField(max_length=255, verbose_name='Project name')
    status = models.CharField(
        max_length=100,
        verbose_name='Order status',
        choices=STATUS_CHOISES,
        default=STATUS_NEW
    )
    order_type = models.CharField(
        max_length=100,
        verbose_name='Order type',
        choices=ORDER_TYPE_CHOIСE,
        default=ORDER_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Order comment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Date of order creation')
    order_date = models.DateField(verbose_name='Date of receipt of the order ', default=timezone.now)

    def __str__(self):
        """Function returns id of order in string formation"""
        return str(self.id)
