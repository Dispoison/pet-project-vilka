from django import forms


class ProductModelForm(forms.ModelForm):

    more_photos = forms.FileField(label='Дополнительные изображения', required=False, widget=forms.FileInput(attrs={
        'multiple': True,
    }))

    class Meta:
        from shop.models import Product
        model = Product
        fields = '__all__'


class AddProductToCartForm(forms.Form):
    quantity = forms.IntegerField(label='Количетсво', initial=1)
