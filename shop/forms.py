from django import forms


class ProductModelForm(forms.ModelForm):

    more_photos = forms.FileField(label='Дополнительные изображения', required=False, widget=forms.FileInput(attrs={
        'multiple': True,
    }))

    # def save(self, commit=True):
    #     if self.request:
    #         product = super(ProductModelForm, self).save(commit=False)
    #         print(self.request)
    #         photos = self.request.FILES.getlist('more_photos')
    #         for photo in photos:
    #             from shop.models import ProductPhoto
    #             ProductPhoto.objects.create(product=product, photo=photo)
    #     return super(ProductModelForm, self).save(commit=commit)

    class Meta:
        from shop.models import Product
        model = Product
        fields = '__all__'
