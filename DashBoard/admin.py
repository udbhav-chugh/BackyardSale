from django.contrib import admin

from .models import Item, Category, SubCategory, NewUser

admin.site.register(Item)
admin.site.register(NewUser)
admin.site.register(Category)
admin.site.register(SubCategory)