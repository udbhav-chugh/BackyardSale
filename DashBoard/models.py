from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class NewUser(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE,primary_key=True)
    PhoneNum= models.CharField(max_length=100)


class Category(models.Model):
    Name = models.CharField(max_length=250)

    def __str__(self):
        return self.Name


class SubCategory(models.Model):
    Name = models.CharField(max_length=250)
    ParentCategory = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


# 0) Item available for Sale
# 1) Item available for Rent
# 2) Item Currently Rented
# 3) Item Sold

class Item(models.Model):
    Category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, related_name="Category", null=True)
    # Can be removed because
    # we can get category from subcategory!
    SubCategory = models.ForeignKey(to=SubCategory, on_delete=models.SET_NULL, related_name="SubCategory", null=True)
    ProductModel = models.CharField(max_length=250)
    ProductImage = models.ImageField()
    ProductPrice = models.DecimalField(decimal_places=2, max_digits=12)
    Negotiable = models.BooleanField(default=True)
    Seller = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Seller")
    CurrentStatus = models.IntegerField()
    RenterInfo = models.ForeignKey(to=User, default=None, on_delete=models.SET_NULL, related_name="Consumer", null=True)
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return self.ProductModel


