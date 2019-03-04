from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import NewUser,Item
# Create your views here.


class dashboard(generic.DetailView):
    model = NewUser
    context_object_name = 'CurrentUser'
    template_name = 'DashBoard/dashboard.html'
    # Slug Field no longer needed, so Removed #

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(dashboard, self).get_context_data(**kwargs)
        context['Items'] = Item.objects.filter(Seller=self.request.user)

        return context

