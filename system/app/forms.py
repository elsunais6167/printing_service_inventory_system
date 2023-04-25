from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'phone', 'address']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
    
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_category', 'buying_price', 'product_quantity']
    
    def __init__(self, *args, **kwargs):
        prod_cat = kwargs.pop('product_category')
        super().__init__(*args, **kwargs)
        self.fields['product_category'].queryset = prod_cat

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = fields = ['service_type', 'service_category', 'service_cost']
    
    def __init__(self, *args, **kwargs):
        service_cat = kwargs.pop('service_category')
        super().__init__(*args, **kwargs)
        self.fields['service_category'].queryset = service_cat

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['products', 'product_price', 'quantity']
        widgets = {
            'products': forms.Select(),
            }
class OfferedForm(ModelForm):
    class Meta:
        model = Offered
        fields = ['service', 'service_cost', 'quantity']