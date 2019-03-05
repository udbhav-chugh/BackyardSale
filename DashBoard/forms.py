from django import forms
from . import models



class ItemForm(forms.ModelForm):
    Status = forms.ChoiceField(choices=[("1","Rent"),("0","Sale")]) # Will change Current Status according to this Status #

    class Meta:
        model = models.Item
        fields=['Category','SubCategory','ProductModel', 'ProductPrice', 'Negotiable', 'Description', 'ProductImage']

    def getCurrStatus(self):
        self.instance.CurrentStatus = self.cleaned_data["Status"]

    def getSeller(self):
        self.instance.Seller = self.request.user

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')
        super(ItemForm, self).__init__(*args, **kwargs)