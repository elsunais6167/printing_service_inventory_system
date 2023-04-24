from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Business)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Offered)
admin.site.register(Sale)