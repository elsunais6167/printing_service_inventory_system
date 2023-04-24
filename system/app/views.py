import re
import pickle
import cgi, cgitb

from django.db.models import Sum
from django.db.models import Count
from django.core.paginator import Paginator
from django.forms import FloatField
from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.style import context
from sqlalchemy import Float
from sympy import total_degree

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm
from .forms import CustomerForm
from .forms import CategoryForm
from .forms import ProductForm
from .forms import SaleForm


from .models import *


# Create your views here.
#@login_required
def index(request):
    '''
    sales_count = Sale.objects.values('user').annotate(total_sales=Count('user'))
    for count in sales_count:
        total_sales = count['total_sales']
    
    prod_count = Product.objects.values('user').annotate(total_products=Count('user'))
    for count in prod_count:
        total_products = count['total_products']
    
    customer_count = Customer.objects.values('user').annotate(total_customers=Count('user'))
    for count in customer_count:
        total_customers = count['total_customers']
    
    labels = []
    data = []

    user_sales = Sale.objects.filter(user=request.user)
    for sale in user_sales:
        labels.append(sale.products.prod_name)
        data.append(sale.quantity * sale.selling_price)
    
    context = {'labels': labels, 
               'data': data, 
               'total_sales': total_sales, 
               'total_products': total_products, 
               'total_customers': total_customers,
               }
               '''
    return render(request, 'index.html')

#@login_required
def sale(request):
    context = {}
    return render(request, 'sale.html', context)

#@login_required
def category(request):
    user = request.user
    categories = Category.objects.filter(user_id=user.id)

    pagination = Paginator(categories, 10)
    page_num = request.GET.get('page')
    pag_obj = pagination.get_page(page_num)

    context = {'pag_obj':pag_obj, 'categories':  categories}
    return render(request, 'category.html', context)

#@login_required
def product(request):
    user = request.user
    products = Product.objects.filter(user_id=user.id)


    pagination = Paginator(products, 10)
    page_num = request.GET.get('page')
    pag_obj = pagination.get_page(page_num)

    context = {'pag_obj':pag_obj, 'products': products}
    return render(request, 'product.html', context)

#@login_required
def add(request):
    user = request.user
    add_prod = Product.objects.filter(user_id=user.id)

    paginator = Paginator(add_prod, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj':page_obj, 'add_prod': add_prod}
    return render(request, 'add.html', context)

#@login_required
def customer(request):
    user = request.user
    customers = Customer.objects.filter(user_id=user.id)

    pagination = Paginator(customers, 10)
    page_num = request.GET.get('page')
    pag_obj = pagination.get_page(page_num)

    context = {'pag_obj':pag_obj, 'customers': customers,}
    return render(request, 'customer.html', context)

#@login_required
def report(request):
    user = request.user
    reports = Sale.objects.filter(user_id=user.id)
    
    pagination = Paginator(reports, 10)
    page_num = request.GET.get('page')
    pag_obj = pagination.get_page(page_num)

    context = {'pag_obj': pag_obj, 'reports': reports}
    return render(request, 'report.html', context)


#@login_required
def sell_pred(request):
    return render(request, 'sell.html')

#@login_required
def prof_pred(request):
    request.GET
    context = {}
    return render(request, 'prof.html', context)


#Settings
@login_required
def profile(request):
    context ={}
    return render(request, 'profile.html', context)

#Forms creations
@login_required
def  create_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            # Create a new product and set the user field
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('customer')

    context = {'form': form}

    return render(request, 'add_customer.html', context)

#@login_required
def create_product(request):
    user = request.user
    # Filter sales by user
    prod_cat = Category.objects.filter(user_id=user.id)
    form = ProductForm(prod_cat=prod_cat)
    if request.method == "POST":
        form = ProductForm(request.POST, prod_cat=prod_cat)
        if form.is_valid():
            # Get the current user
            user = request.user
            # Create a new product and set the user field
            product = form.save(commit=False)
            product.user = user
            product.save()
            return redirect('product')

    context = {'form': form}

    return render(request, 'add_product.html', context)

#@login_required
def  create_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            user = request.user
            # Create a new product and set the user field
            category = form.save(commit=False)
            category.user = user
            category.save()
    
            return redirect('category')

    context = {'form': form}

    return render(request, 'add_category.html', context)


#@login_required
def  sale_item(request):
    user = request.user
    # Filter sales by user
    prod = Product.objects.filter(user_id=user.id)
    form = SaleForm(products=prod)
    if request.method == "POST":
        form = SaleForm(request.POST, products=prod)
        if form.is_valid():
            user = request.user
            # Create a new product and set the user field
            sale = form.save(commit=False)
            sale.user = user
            sale.save()
            
            return redirect('sale_item')

    context = {'form': form}

    return render(request, 'add_sale.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ('Invalid Username or Password, Please Try Again!'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def log_out(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Succesful. You are now logged in")
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})