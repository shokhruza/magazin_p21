from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, IntegerField, PositiveIntegerField, ForeignKey, CASCADE, \
    SmallIntegerField, SlugField, ImageField, ManyToManyField, JSONField, DateTimeField, CheckConstraint, Q
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class User(AbstractUser):
    image = ImageField(upload_to='users/', null=True, blank=True)


class Category(MPTTModel):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    discount = SmallIntegerField()
    description = CKEditor5Field()
    quantity = PositiveIntegerField()
    shipping_cost = IntegerField()
    specifications = JSONField(default=dict, blank=True)
    author = ForeignKey('apps.User', CASCADE, related_name='products')
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    tags = ManyToManyField('apps.Tag', blank=True)
    created_at = DateTimeField(auto_now_add=True)

    @property
    def current_price(self):
        return self.price - self.price * self.discount / 100

    def __str__(self):
        return self.name


class Review(Model):
    title = CharField(max_length=255)
    product = ForeignKey('apps.Product', CASCADE, related_name='reviews')
    author = ForeignKey('apps.User', CASCADE, related_name='reviews')
    rating = SmallIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rating__gte=0) & Q(rating__lte=10), name='rating_between_0_10'),
        ]


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    created_at = DateTimeField(auto_now_add=True)


class Tag(Model):
    name = CharField(max_length=255)


class Order(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    created_at = DateTimeField(auto_now_add=True)


class Cart(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='user_carts')
    product = ForeignKey('apps.User', CASCADE, related_name='carts')
    created_at = DateTimeField(auto_now_add=True)


class OrderItem(Model):
    order = ForeignKey('Order', CASCADE, related_name='items')
    product = ForeignKey('apps.Product', CASCADE, related_name='items')
    quantity = PositiveIntegerField(default=1, db_default=1)


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=5)
