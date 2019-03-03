from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from DashBoard.models import Category, SubCategory, Item
from django.http import HttpResponse

class homeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'Categories'

    def get_context_data(self, **kwargs):
        context = super(homeView, self).get_context_data(**kwargs)
        context['SubCategories'] = SubCategory.objects.all()
        return context

    def get_queryset(self):
        return Category.objects.all()

class subCategoryView(generic.DetailView):
    model = SubCategory
    context_object_name = 'SubCat'
    template_name = 'subDetail.html'
    slug_url_kwarg = 'slug'
    slug_field = 'Name'

    def get_context_data(self, **kwargs):
        context = super(subCategoryView, self).get_context_data(**kwargs)
        context['Items'] = Item.objects.filter(SubCategory__Name=self.kwargs['slug'])
        return context


def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(to=request.GET.get('next'))
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request,'registration/login.html', {'error_message':"Invalid Username Password"})
    else:
        return render(request,'registration/login.html')

def logoutUser(request):
    pass