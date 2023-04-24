from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DateField

# Create your models her
class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    logo = models.ImageField(upload_to='profile/')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=50, null=True)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category_name = models.CharField(max_length=50, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, db_column='category_name', null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=50, null=True)
    buying_price = models.IntegerField()
    selling_price = models.IntegerField()
    product_quantity = models.IntegerField()
    product_image = models.ImageField(upload_to='products/', null=True)
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name
    
class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_category = models.ForeignKey(Category, db_column='category_name', null=True, on_delete=models.SET_NULL)
    service_type = models.CharField(max_length=50, null=True)
    service_cost = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.service_type

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Product, db_column='product_name', null=True, on_delete=models.SET_NULL, related_name='sale_products')
    product_price = models.ForeignKey(Product, db_column='selling_price', null=True, on_delete=models.SET_NULL, related_name='sale_product_prices')
    quantity = models.IntegerField()
    date_created = DateField(auto_now_add=True)

    def __str__(self):
        return self.products
    
    @property
    def Total_sales(self):
        sales = self.selling_price
        quant = self.quantity
        total = sales * quant
        return total

class Offered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, db_column='service_type', null=True, on_delete=models.SET_NULL, related_name='offered_service')
    service_cost = models.ForeignKey(Service, db_column='service_cost', null=True, on_delete=models.SET_NULL, related_name='offered_service_cost')
    quantity = models.IntegerField()
    date_created = DateField(auto_now_add=True)

    def __str__(self):
        return self.service
    
    @property
    def Total_offer(self):
        sales = self.service_cost
        quant = self.quantity
        total = sales * quant
        return total