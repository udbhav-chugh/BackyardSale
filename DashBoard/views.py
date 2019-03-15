from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import ItemForm, verifyOTP
from .models import NewUser, Item, SubCategory
from BackyardSale.views import updateTransactionItems
from django.contrib import messages


# Create your views here.


class dashboard(generic.DetailView):

    model = NewUser
    context_object_name = 'CurrentUser'
    template_name = 'DashBoard/dashboard.html'

    def get(self, request, *args, **kwargs):
        try:
            return super(dashboard, self).get(request,*args,**kwargs)
        except Http404:
            return redirect(to='/completedetails')



    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(dashboard, self).get_context_data(**kwargs)
        updateTransactionItems()
        context['ItemsListed'] = Item.objects.filter(Seller=self.request.user, CurrentStatus__range=[0,1]) # Check for range #
        context['ItemsSold'] = Item.objects.filter(Seller=self.request.user, CurrentStatus=2)
        context['ItemsRented'] = Item.objects.filter(Seller=self.request.user, CurrentStatus=3)
        context['RentedItemsbyMe'] = Item.objects.filter(RenterInfo=self.request.user, CurrentStatus=3)
        context['BoughtItems'] = Item.objects.filter(RenterInfo=self.request.user, CurrentStatus=2)

        return context


class createItem(generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'DashBoard/createItem.html'
    success_url = reverse_lazy('Dashboard:dashboard')

    def form_valid(self, form):
        form.getCurrStatus()
        form.getSeller()
        return super(createItem, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(createItem, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


def getSubCategories(request):
    cat_id = request.GET.get('Category')
    if cat_id == "":
        SubCategories = SubCategory.objects.none()
    else:
        SubCategories = SubCategory.objects.filter(ParentCategory_id=cat_id)

    return render(request, 'DashBoard/categoryDropdown.html', {"SubCategories": SubCategories})


class deleteItems(generic.DeleteView):
    model = Item
    success_url = reverse_lazy('Dashboard:dashboard')

    def get(self, **kwargs):
        if (self.request.user != self.get_object().Seller or self.get_object().CurrentStatus > 1):
            raise Http404('Page doesn\'t exist')
        else:
            super(deleteItems, self).get(**kwargs)


class updateItems(generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'DashBoard/createItem.html'
    success_url = reverse_lazy('Dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.getCurrStatus()
        form.getSeller()
        return super(updateItems, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(updateItems, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


class approveView(generic.ListView):
    template_name = 'DashBoard/pendingTransactions.html'
    context_object_name = 'Items'

    def get_queryset(self):
        return Item.objects.filter(CurrentStatus__range=[4,6], Seller=self.request.user)

class approveItem(generic.FormView):
    form_class = verifyOTP
    template_name = 'DashBoard/approveItem.html'
    success_url = reverse_lazy('Dashboard:dashboard')


    def form_valid(self, form):
        current_item = get_object_or_404(Item,pk=self.kwargs['pk'])

        if(current_item.otp == form.cleaned_data['OTP']):
            if(current_item.CurrentStatus == 4 or current_item.CurrentStatus == 5):
                current_item.CurrentStatus -= 2
            current_item.otp = None
            current_item.otpExpiryTime = None
            current_item.save()
            return super(approveItem, self).form_valid(form=form)
        else:
            form.add_error('OTP',"Invalid OTP")
            context = self.get_context_data()
            context['form'] = form
            return render(self.request,'DashBoard/approveItem.html',context)


    def get_context_data(self, **kwargs):
        context = super(approveItem, self).get_context_data()
        current_item = get_object_or_404(Item,pk=self.kwargs['pk'])
        context['Item'] = current_item
        return context











