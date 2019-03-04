from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from DashBoard.models import Category, SubCategory, Item
from . import forms



class homeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'Categories'

    def get_context_data(self, **kwargs):
        context = super(homeView, self).get_context_data(**kwargs) # Calling Base Class to get the original context data #
        context['SubCategories'] = SubCategory.objects.all() # Adding SubCategories to the context #
        return context

    def get_queryset(self):
        return Category.objects.all()

class subCategoryView(generic.DetailView):
    model = SubCategory
    context_object_name = 'SubCat'
    template_name = 'subDetail.html'
    slug_field = 'Name'

    def get_context_data(self, **kwargs):
        context = super(subCategoryView, self).get_context_data(**kwargs) # Calling the Base method to get the original context data #
        context['Items'] = Item.objects.filter(SubCategory=self.object) # Adding Items to the context #
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