from django import forms
from . import models


class ItemForm(forms.ModelForm):
    Status = forms.ChoiceField(choices=[("0", "Sale"), ("1", "Rent")])  # Will change Current Status according to this Status #

    class Meta:
        model = models.Item
        fields = ['Category', 'SubCategory', 'ProductModel', 'ProductPrice', 'Negotiable', 'Description', 'ProductImage']

    def getCurrStatus(self):
        self.instance.CurrentStatus = self.cleaned_data["Status"]

    def getSeller(self):
        self.instance.Seller = self.request.user

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['SubCategory'].queryset = models.SubCategory.objects.none()

        if 'Category' in self.data:
            try:
                Category = int(self.data.get('Category'))
                self.fields['SubCategory'].queryset = models.SubCategory.objects.filter(ParentCategory_id=Category).order_by('Name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['SubCategory'].queryset = models.SubCategory.objects.filter(ParentCategory=self.instance.Category)


class verifyOTP(forms.Form):
    OTP = forms.IntegerField(min_value=100000, max_value=999999)