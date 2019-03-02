from django.contrib import admin
from .models import Item, Category, SubCategory, NewUser
import django.contrib.auth.admin


admin.site.register(Item)
admin.site.register(NewUser)
admin.site.register(Category)
admin.site.register(SubCategory)