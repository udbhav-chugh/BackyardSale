from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse,get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from DashBoard.models import Category, SubCategory, Item, NewUser
from . import forms
from django.utils import timezone
from datetime import timedelta
import random



class homeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'Categories'

    def get_context_data(self, **kwargs):
        context = super(homeView, self).get_context_data(**kwargs) # Calling Base Class to get the original context data #
        updateTransactionItems()
        context['SubCategories'] = SubCategory.objects.all() # Adding SubCategories to the context #
        return context

    def get_queryset(self):
        return Category.objects.all()

class subCategoryView(generic.DetailView):
    model = SubCategory
    context_object_name = 'SubCat'
    template_name = 'viewItems.html'

    def get_context_data(self, **kwargs):
        context = super(subCategoryView, self).get_context_data(**kwargs) # Calling the Base method to get the original context data #
        updateTransactionItems()
        context['Items'] = Item.objects.filter(SubCategory=self.object, CurrentStatus__lte=1) # Adding Items to the context #
        return context


class CategoryView(generic.DetailView):
    model = Category
    context_object_name = 'Category'
    template_name = 'viewItems.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs) # Calling the Base method to get the original context data #
        updateTransactionItems()
        context['Items'] = Item.objects.filter(Category=self.object, CurrentStatus__lte=1)  # Adding Items to the context #
        return context


class ItemView(generic.DetailView):
    model = Item
    context_object_name = 'Item'
    template_name = 'itemdetails.html'

def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(to=request.GET.get('next','/'))
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request,'registration/login.html', {'error_message':"Invalid Username Password"})
    else:
        return render(request,'registration/login.html')

def logoutUser(request):
    logout(request)
    return  redirect(to="/")



def register(request):
    userForm = forms.UserForm(request.POST or None)
    userInfoForm = forms.UserInfoForm(request.POST or None)
    if userForm.is_valid() and userInfoForm.is_valid():
        user=userForm.save(commit=False)
        userInfo=userInfoForm.save(commit=False)
        username = userForm.cleaned_data['username']
        password = userForm.cleaned_data['password']
        user.set_password(password)
        user.save()
        userInfo.user=user
        userInfo.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to='/')

    context={
        'userForm' : userForm,
        'userInfoForm': userInfoForm,
    }
    return render(request,'registration/register.html',context)


def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''


    Items = Item.objects.filter(ProductModel__contains=search_text, CurrentStatus__lte=1)
    Categories = Category.objects.filter(Name__contains=search_text)
    SubCategories = SubCategory.objects.filter(Name__contains=search_text)

    context = {
        'Items' : Items,
        'Categories': Categories,
        'SubCategories': SubCategories,
        'search_text': search_text,
    }

    return render(request,'getResults.html',context)


def ItemBuy(request,slug,pk):
    otp = random.randint(100000, 999999)
    now= timezone.now()
    current_item=get_object_or_404(Item,pk=pk)
    current_item.otp=otp
    current_item.otpExpiryTime=now+timedelta(days=1)
    current_item.CurrentStatus+=4
    current_item.save()
    return HttpResponse("Otp generated successfully")


def updateTransactionItems():
    inTransactionItems = Item.objects.filter(CurrentStatus__range=[4, 6])
    for x in inTransactionItems:
        x.withinTransaction()