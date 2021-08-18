from django import forms


class ProductModelForm(forms.ModelForm):

    more_photos = forms.FileField(label='Дополнительные изображения', required=False, widget=forms.FileInput(attrs={
        'multiple': True,
    }))

    class Meta:
        from shop.models.products.product import Product
        model = Product
        fields = '__all__'


class DisplayOptionsForm(forms.Form):
    sort_choices = (('0', 'от дорогих'), ('1', 'от дешевых'))
    display_num_choices = (('0', '3'), ('1', '6'), ('2', '9'))
    sort = forms.ChoiceField(choices=sort_choices, label='Сортировка')
    display_num = forms.ChoiceField(choices=display_num_choices, label='Количество')
