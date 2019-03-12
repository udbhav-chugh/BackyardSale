from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.

class NewUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    PhoneNum = models.CharField(max_length=100)
    Address = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    Name = models.CharField(max_length=250)
    slug = models.SlugField()

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    Name = models.CharField(max_length=250)
    ParentCategory = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Name)
        super(SubCategory, self).save(*args, **kwargs)


# Current Status
# 0) Item available for Sale
# 1) Item available for Rent
# 2) Item Currently Rented
# 3) Item Sold
# 4) In Transaction for Sale
# 5) In Transaction for Rent

class Item(models.Model):
    Category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, related_name="Category", null=True)
    # Can be removed because
    # we can get category from subcategory!
    SubCategory = models.ForeignKey(to=SubCategory, on_delete=models.SET_NULL, related_name="SubCategory", null=True)
    ProductModel = models.CharField(max_length=250)
    ProductImage = models.ImageField()
    ProductPrice = models.DecimalField(decimal_places=2, max_digits=12)
    Negotiable = models.BooleanField(default=False)
    Seller = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Seller")
    CurrentStatus = models.IntegerField()
    RenterInfo = models.ForeignKey(to=User, default=None, on_delete=models.SET_NULL, related_name="Consumer", null=True, blank=True)
    Description = models.CharField(max_length=1000, default=None, blank=True)
    slug = models.SlugField()
    otp = models.IntegerField(null=True, blank=True,default=0)
    otpExpiryTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ProductModel

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ProductModel)
        super(Item, self).save(*args, **kwargs)

    def withinTransaction(self):
        now = timezone.now()
        if(now > self.otpExpiryTime):
            self.otp = None
            self.otpExpiryTime = None # Arithmetic Error Possible
            self.CurrentStatus = self.CurrentStatus - 4
            self.save()
            return False

        return True

