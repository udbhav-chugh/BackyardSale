from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse,get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from DashBoard.models import Category, SubCategory, Item, NewUser, RequestedItems
from . import forms
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.decorators import login_required


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

    def get_object(self, queryset=None):
        obj=super(ItemView, self).get_object()

        if(obj.CurrentStatus > 1 and obj.Seller != self.request.user and obj.RenterInfo != self.request.user):
            raise Http404("This Page doesn't Exist")
        else:
            return obj

# Incase koi problem aaye try to add backend #
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


def completeDetails(request):
    userForm = forms.PasswordForm(request.POST or None)
    userInfoForm = forms.UserInfoForm(request.POST or None)
    if userForm.is_valid() and userInfoForm.is_valid():
        current_user=request.user
        current_user.set_password(userForm.cleaned_data['password'])
        login(request,current_user, backend='django.contrib.auth.backends.ModelBackend')
        current_user.save()
        userInfo = userInfoForm.save(commit=False)
        userInfo.user = current_user
        userInfo.save()
        return redirect(to=reverse_lazy('home'))

    context = {
        'userForm': userForm,
        'userInfoForm': userInfoForm,
    }
    return render(request, 'registration/completedetail.html', context)


def updateuser(request):
    userForm = forms.updateUser(request.POST or None, instance=request.user)
    userInfoForm = forms.UserInfoForm(request.POST or None, instance=NewUser.objects.get(user=request.user))
    if userForm.is_valid() and userInfoForm.is_valid():
        current_user=request.user
        current_user.first_name = userForm.cleaned_data['first_name']
        current_user.last_name = userForm.cleaned_data['last_name']
        current_user.email = userForm.cleaned_data['email']
        current_user.set_password(userForm.cleaned_data['password'])
        login(request,current_user, backend='django.contrib.auth.backends.ModelBackend')
        current_user.save()
        userInfo = userInfoForm.save(commit=False)
        userInfo.user = current_user
        userInfo.save()
        return redirect(to='/')

    context = {
        'userForm': userForm,
        'userInfoForm': userInfoForm,
    }
    return render(request, 'registration/register.html', context)


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
    if request.user.is_authenticated:
        otp = random.randint(100000, 999999)
        now= timezone.now()
        current_item=get_object_or_404(Item,pk=pk)


        if(current_item.CurrentStatus > 1):
            raise Http404("This page doesn't exist")


        if (current_item.Seller == request.user):
            raise Http404("Lister cannot buy his/her own product")


        current_item.otp=otp
        current_item.otpExpiryTime=now+timedelta(days=1)
        current_item.RenterInfo = request.user

        if(current_item.CurrentStatus == 0):
            current_item.CurrentStatus = 4
        elif(current_item.CurrentStatus == 1):
            current_item.CurrentStatus = 5

        current_item.save()
        return HttpResponse("Otp generated successfully" + " OTP is " + str(otp))
    else:
        return redirect(to='/login/?next='+request.path)


def updateTransactionItems():
    inTransactionItems = Item.objects.filter(CurrentStatus__range=[4, 6])
    for x in inTransactionItems:
        x.withinTransaction()

def contactus(request):
    return render(request,'contactus.html')

class createRequest(generic.CreateView):
    model = RequestedItems
    form_class = forms.RequestItem
    template_name = 'requestItem.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.getRequester(self.request)
        return super(createRequest, self).form_valid()
